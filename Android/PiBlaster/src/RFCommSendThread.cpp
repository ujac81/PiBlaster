

#include "RFCommSendThread.h"
#include "RFCommMaster.h"

#include <QtDebug>

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#else
    #include "RFCommMessageObject.h"
    RFCommMessageObject* CreateDummyResponse( int id, const QString& cmd,
                                              const QList<QString>& payload );
#endif


RFCommSendThread::RFCommSendThread( RFCommMaster *parent, int id,
                                    const QString& msg,
                                    const QList<QString>& payload ) :
    QThread( dynamic_cast<QObject*>(parent) ),
    _parent( parent ),
    _id( id ),
    _cmd( msg ),
    _payload( payload )
{
    _sendDone = false;
}


void RFCommSendThread::run()
{

#ifndef DUMMY_MODE

    QString cmd = QString::number( _id ) + " " +
            QString::number( _payload.size() ) + " " +  _cmd;
    qDebug() << "Sending " << cmd;

    QString head = QString("%1").arg(QString::number(cmd.length()), 4, '0');

    QAndroidJniObject javaCommand = QAndroidJniObject::fromString( head + cmd );
    int sendOk = QAndroidJniObject::callStaticMethod<jint>(
                "org/piblaster/piblaster/rfcomm/RfcommClient",
                "sendLine", "(Ljava/lang/String;)I",
                javaCommand.object<jstring>() );

    for ( int i = 0; i < _payload.size(); ++i )
    {
        QString line = _payload[i];
        QString head = QString("%1").arg(
                    QString::number( line.length()), 4, '0');
        QAndroidJniObject javaCommand =
                QAndroidJniObject::fromString( head + line );
        sendOk = QAndroidJniObject::callStaticMethod<jint>(
                        "org/piblaster/piblaster/rfcomm/RfcommClient",
                        "sendLine", "(Ljava/lang/String;)I",
                        javaCommand.object<jstring>() );

        if ( sendOk != 0 ) break;
    }

    if ( sendOk == 0 )
        emit commandSent( _cmd );
    else
        emit commBroken( sendOk );
#else

    emit commandSent( _cmd );

    RFCommMessageObject* msg = CreateDummyResponse( _id, _cmd, _payload );
    emit gotMessage( *msg );
    delete msg;

#endif

    _sendDone = true;
}
