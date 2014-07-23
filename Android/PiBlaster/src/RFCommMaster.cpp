
#include "RFCommMaster.h"

#include "RFCommSendThread.h"
#include "RFCommRecvThread.h"

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#endif

#include <QTimer>


RFCommMaster::RFCommMaster( QObject* parent ) :
    QObject( parent ),
    _msgId( 0 )
{
    _recv = NULL;
}


RFCommMaster::~RFCommMaster()
{
    qDebug() << "DTOR: RFCommMaster";
    if ( _recv )
    {
        _recv->abort();
        _recv->wait();
        delete _recv;
    }
    cleanSendQueue( true );
}


void RFCommMaster::checkBluetoothOn()
{
#ifndef DUMMY_MODE
    QAndroidJniObject::callStaticMethod<void>(
                "org/piblaster/piblaster/rfcomm/RfcommClient", "onInit" );
#endif
    callBluetoothState();
}


void RFCommMaster::callBluetoothState()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>(
                "org/piblaster/piblaster/rfcomm/RfcommClient",
                "bluetoothConnectionStatus");
    emit bluetoothState( res );
#else
    emit bluetoothState( 2 );
#endif
}


int RFCommMaster::connectBluetooth()
{
    // this is ok, if there is a receiver thread from an old run,
    // this one leave its receiver loop now. On successful connect,
    // a new receiver thread will be created.
    if ( _recv ) _recv->abort();

    qDebug() << "tryConnect()";
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>(
                "org/piblaster/piblaster/rfcomm/RfcommClient", "connect");
    qDebug() << "tryConnect() return: " << res;

    if ( res == 2 ) generateReceiveThread();

    return res;
#else
    return 2;
#endif
}


void RFCommMaster::gotMessage( RFCommMessageObject msg )
{
    if ( msg.code() == 1000 )
    {
        // got OK on keepalive --> do nothing
        return;
    }
    // PRO: payload is split here to save memory
    // CON: This thread may block the main APP while splitting.
    msg.preparePayloadElements();
    emit receivedMessage( &msg );

    // check if we may delete send instances
    cleanSendQueue();
}


void RFCommMaster::keepAlive()
{
    execCommand( "keepalive" );
    // send next keep alive 10 secs later
    QTimer::singleShot( 10000, this, SLOT( keepAlive() ) );
}


void RFCommMaster::execCommand( const QString& command )
{
    if ( ! waitForSend() )
    {
        qDebug() << "RFCommMaster::execCommand(): send queue not empty for "
                 << command;
        return;
    }

    _msgId++;
    RFCommSendThread* send = new RFCommSendThread( this, _msgId, command );
    connect( send, &RFCommSendThread::commandSent, this,
             &RFCommMaster::commandSent );
    connect( send, &RFCommSendThread::commBroken, this,
             &RFCommMaster::commBroken );
#ifdef DUMMY_MODE
    connect( send, &RFCommSendThread::gotMessage, this,
             &RFCommMaster::gotMessage );
#endif
    send->start();
    _sendQueue.push_back( send );
}


void RFCommMaster::execCommandWithPayload( const QString& command )
{
    if ( ! waitForSend() )
    {
        qDebug() << "RFCommMaster::execCommand(): send queue not empty for "
                 << command;
        return;
    }

    _msgId++;
    RFCommSendThread* send = new RFCommSendThread( this, _msgId, command,
                                                   _sendPayload );
    connect( send, &RFCommSendThread::commandSent, this,
             &RFCommMaster::commandSent );
    connect( send, &RFCommSendThread::commBroken, this,
             &RFCommMaster::commBroken );

#ifdef DUMMY_MODE
    connect( send, &RFCommSendThread::gotMessage, this,
             &RFCommMaster::gotMessage );
#endif
    send->start();
    _sendQueue.push_back( send );
}


void RFCommMaster::cleanSendQueue( bool forceClean )
{
    std::deque<RFCommSendThread*> tmpQueue = _sendQueue;
    _sendQueue.clear();
    for ( unsigned i = 0; i < tmpQueue.size(); ++i )
    {
        if ( tmpQueue[i] )
        {
            // check if send done
            if ( tmpQueue[i]->sendDone() )
            {
                tmpQueue[i]->wait();
                delete tmpQueue[i];
                tmpQueue[i] = NULL;
            }

            if ( tmpQueue[i] && forceClean )
            {
                // Aggressively shut down send thread (e.g. on exit).
                // Give another 500ms to finish -- terminate after that
                if ( ! tmpQueue[i]->wait( 500 ) )
                {
                    tmpQueue[i]->terminate();
                    delete tmpQueue[i];
                    tmpQueue[i] = NULL;
                }
            }


            if ( tmpQueue[i] )
            {
                // active send in progress, keep instance
                _sendQueue.push_back( tmpQueue[i] );
            }
        }
    }
}


bool RFCommMaster::waitForSend( int ms )
{
    bool sendOk = true;
    for ( unsigned i = 0; i < _sendQueue.size(); ++i )
    {
        if ( _sendQueue[i] )
        {
            if ( ! _sendQueue[i]->wait( ms ) )
            {
                sendOk = false;
            }
        }
    }

    cleanSendQueue();
    return sendOk;
}


void RFCommMaster::generateReceiveThread()
{
    qmlRegisterType<RFCommMessageObject>();

    // should not happen!
    /// @todo let master clean out receive thread on disconnect
    if ( _recv )
    {
        qDebug() << "WARNING() RFCommMaster::generateReceiveThread(): "
                 << "while another recv thread still active -- shutting "
                 << "down other thread...";
        _recv->abort();
        _recv->wait();
        delete _recv;
        _recv = NULL;
    }

    _recv = new RFCommRecvThread( this );
    connect( _recv, &RFCommRecvThread::commBroken, this,
             &RFCommMaster::commBroken );
    connect( _recv, &RFCommRecvThread::bluetoothMessage, this,
             &RFCommMaster::bluetoothMessage );

    // No signal-signal connection here -
    // use of buffer to copy message might be required,
    // need to send pointer to QML, not object.
    // Real object is destroyed in thread after sending.
    connect( _recv, &RFCommRecvThread::gotMessage, this,
             &RFCommMaster::gotMessage );
    _recv->start();

    // send keepalive in 10 secs
    QTimer::singleShot( 10000, this, SLOT( keepAlive() ) );
}



