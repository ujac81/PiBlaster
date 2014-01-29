
#include "RFCommMaster.h"

#include "RFCommSendThread.h"
#include "RFCommRecvThread.h"

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#endif


RFCommMaster::RFCommMaster( QObject* parent ) :
    QObject( parent ),
    _msgId( 0 )
{
    _recv = NULL;
}


RFCommMaster::~RFCommMaster()
{
    // do not delete _recv here, Qt will do.
}


void RFCommMaster::checkBluetoothOn()
{
#ifndef DUMMY_MODE
    QAndroidJniObject::callStaticMethod<void>( "org/piblaster/piblaster/rfcomm/RfcommClient", "onInit" );
#endif
    callBluetoothState();
}


void RFCommMaster::callBluetoothState()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
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
    jint res = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                                         "connect");
    qDebug() << "tryConnect() return: " << res;

    if ( res == 2 ) generateReceiveThread();

    return res;
#else
    return 2;
#endif
}


void RFCommMaster::execCommand( const QString& command )
{
    _msgId++;
    RFCommSendThread* send = new RFCommSendThread( this, _msgId, command );
    connect( send, &RFCommSendThread::commandSent, this, &RFCommMaster::commandSent );
    connect( send, &RFCommSendThread::commBroken, this, &RFCommMaster::commBroken );
    connect( send, &RFCommSendThread::finished, send, &QObject::deleteLater );
    send->start();
}


void RFCommMaster::generateReceiveThread()
{
    // It is ok, not to care about destruction here.
    // Qt takes care of destroying the object.

    qmlRegisterType<RFCommMessageObject>();

    _recv = new RFCommRecvThread( this );
    connect( _recv, &RFCommRecvThread::gotMessage, this, &RFCommMaster::gotMessage );
    connect( _recv, &RFCommRecvThread::commBroken, this, &RFCommMaster::commBroken );
    connect( _recv, &RFCommRecvThread::bluetoothMessage, this, &RFCommMaster::bluetoothMessage );
    connect( _recv, &RFCommRecvThread::finished, _recv, &QObject::deleteLater );
    _recv->start();

}



