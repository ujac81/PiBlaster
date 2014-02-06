
#include "RFCommRecvThread.h"
#include "RFCommMaster.h"

#include <QStringList>

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#endif

#include <cassert>

RFCommRecvThread::RFCommRecvThread( RFCommMaster* parent ) :
    QThread( dynamic_cast<QObject*>(parent) ),
    _parent( parent )
{
    qDebug() << "RFCommRecvThread new";
}


RFCommRecvThread::~RFCommRecvThread()
{
    qDebug() << "RFCommRecvThread delete";
}


RFCommMessageObject* RFCommRecvThread::newMessageObject( int id, int status, int code, int plSize, const QString& msg )
{
    assert( _recvBuffer.find( id ) == _recvBuffer.end() );

    RFCommMessageObject* newMsg = new RFCommMessageObject( id, status, code, plSize, msg );
    _recvBuffer[id] = newMsg;
    return newMsg;
}


void RFCommRecvThread::messageDone( int id, RFCommMessageObject* msg )
{
    assert( _recvBuffer.find( id ) != _recvBuffer.end() );
    assert( msg->payloadComplete() );

    emit gotMessage( *msg );
    delete msg;
    _recvBuffer.erase( id );
}


void RFCommRecvThread::abort()
{
    qDebug() << "RFCommRecvThread aborted.";
    _run = false;
}


void RFCommRecvThread::run()
{
    _run = true;

    qDebug() << "RFCommRecvThread started.";

    while( _run )
    {
        QThread::msleep( PollTime );
#ifndef DUMMY_MODE
        // check if message in queue
        QAndroidJniObject string = QAndroidJniObject::callStaticObjectMethod(
                    "org/piblaster/piblaster/rfcomm/RfcommClient",
                    "readLine", "()Ljava/lang/String;" );

        // check if bluetooth comm broken while waiting for new message
        jint res = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                                             "bluetoothConnectionStatus");

        if ( res != 2 )
        {
            qDebug() << ".. lost connection in receiver thread ..";
            _run = false;
            emit commBroken( res );
        }

        // check for bluetooth messages and emit them;
        while (1)
        {
            jint num = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                                                 "numBluetoothMessages");
            if ( num == 0 ) break;
            QAndroidJniObject string = QAndroidJniObject::callStaticObjectMethod(
                        "org/piblaster/piblaster/rfcomm/RfcommClient",
                        "popBluetoothMessages", "()Ljava/lang/String;" );
            emit bluetoothMessage( string.toString() );
        }


        // While receiving multiple lines may be joined if '\n' does not work as seperator.
        // So each line is finished by !EOL! string to separate lines.
        // Each line starts with command id, followed by command type, payload size and message if
        // new command or payload line if payload message
        QStringList lines = string.toString().split( " !EOL! ", QString::SkipEmptyParts );
        for ( int i = 0; i < lines.size(); ++i )
        {
            QStringList elements = lines[i].split( ' ' );
            if ( elements.isEmpty() ) continue;
            int id = elements.takeFirst().toInt();

            std::map<int, RFCommMessageObject*>::iterator iter = _recvBuffer.find( id );
            if ( iter == _recvBuffer.end() )
            {
                // new message received.
                // 1st line should be [id status code payload_length message]
                int status = elements.takeFirst().toInt();
                int code = elements.takeFirst().toInt();
                int plSize = elements.takeFirst().toInt();
                QString msg = elements.join( " " );

                RFCommMessageObject* msgObj = newMessageObject( id, status, code, plSize, msg );

                if ( msgObj->payloadComplete() )
                    messageDone( id, msgObj );
            }
            else
            {
                QString msg = elements.join( " " );
                iter->second->addPayload( msg );
                if ( iter->second->payloadComplete() )
                    messageDone( id, iter->second );
            }
        }
#endif

    } // while run


    qDebug() << "RFCommRecvThread(): loop exit";
}
