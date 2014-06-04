
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


        QString line = string.toString();
        if ( line.length() < 4 ) continue;

        if ( line.left(2) == "PL" )
        {
            // header is PL%4d % n_lines
            int lines = line.mid(2, 4).toInt();
            line.remove(0, 6);

            for ( int i = 0; i < lines; i++ )
            {
                int length = line.left(4).toInt();
                line.remove(0, 4);
                int id = line.left(4).toInt();
                line.remove(0, 4);
                QString subLine = line.left(length-4);
                line.remove(0, length-4);

                std::map<int, RFCommMessageObject*>::iterator iter = _recvBuffer.find( id );
                if ( iter != _recvBuffer.end() )
                {
                    iter->second->addPayload( subLine );
                    if ( iter->second->payloadComplete() )
                        messageDone( id, iter->second );
                }
                else
                {
                    // error, no message object
                }
            }
        }
        else
        {
            // new instruction
            // 1st line should be [id status code payload_length message]
            int id = line.left(4).toInt();
            int status  = line.mid(4, 4).toInt();
            int code    = line.mid(8, 4).toInt();
            int plSize  = line.mid(12, 6).toInt();
            QString msg = line.right(line.length()-18);
            RFCommMessageObject* msgObj = newMessageObject( id, status, code, plSize, msg );
            if ( msgObj->payloadComplete() )
                messageDone( id, msgObj );
        }
#endif
    } // while run

    qDebug() << "RFCommRecvThread(): loop exit";
}
