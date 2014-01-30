

#include "RFCommSendThread.h"
#include "RFCommMaster.h"

#include <QtDebug>

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#endif


RFCommSendThread::RFCommSendThread( RFCommMaster *parent, int id, const QString& msg ) :
    QThread( dynamic_cast<QObject*>(parent) ),
    _parent( parent ),
    _id( id ),
    _cmd( msg )
{}


void RFCommSendThread::run()
{

    qDebug() << "Sending " << _id << " " << _cmd;

#ifndef DUMMY_MODE

    QString cmd = QString::number( _id ) + " " + _cmd;

    QAndroidJniObject javaCommand = QAndroidJniObject::fromString( cmd );
    int sendOk = QAndroidJniObject::callStaticMethod<jint>(
                "org/piblaster/piblaster/rfcomm/RfcommClient",
                "sendLine", "(Ljava/lang/String;)I", javaCommand.object<jstring>() );


    if ( sendOk == 0 )
        emit commandSent( _cmd );
    else
        emit commBroken( sendOk );



#endif

}
