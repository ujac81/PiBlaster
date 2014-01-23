

#include "RFCommThread.h"
#include "RFCommClient.h"

#include <QtDebug>

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#endif

RFCommThread::RFCommThread(RFCommClient *parent) :
    QThread( dynamic_cast<QObject*>(parent) ),
    _parent( parent )
{}


void RFCommThread::run()
{

#ifndef DUMMY_MODE

    QString initCommand = "plappendmultiple " +
            QString::number( _parent->playlistAddMode() ) + " " +
            QString::number( _parent->playlistAddItems().size() );


    qDebug() << "Sending " << initCommand;

    QAndroidJniObject javaCommand = QAndroidJniObject::fromString( initCommand );
    int sendOk = QAndroidJniObject::callStaticMethod<jint>(
                "org/piblaster/piblaster/rfcomm/RfcommClient",
                "prepareMassSend", "(Ljava/lang/String;)I", javaCommand.object<jstring>() );
    if ( sendOk != 0 )
    {
        _parent->setStatusMessage( "Communication broken!" );
        emit gotReply( 2 );
        return;
    }


    for ( int i = 0; i < _parent->playlistAddItems().size(); ++i )
    {
        QAndroidJniObject javaCommand = QAndroidJniObject::fromString( _parent->playlistAddItems()[i] );
        int sendOk = QAndroidJniObject::callStaticMethod<jint>(
                    "org/piblaster/piblaster/rfcomm/RfcommClient",
                    "sendSingleRow", "(Ljava/lang/String;)I", javaCommand.object<jstring>() );
        if ( sendOk != 0 )
        {
            _parent->setStatusMessage( "Communication broken!" );
            emit gotReply( 2 );
            return;
        }
    }

    jint res = QAndroidJniObject::callStaticMethod<jint>( "org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "waitForMassCommand()" );
    if ( res != 2 )
    {
        _parent->setStatusMessage( "Communication broken!" );
        emit gotReply( 2 );
        return;
    }

    QAndroidJniObject string1 = QAndroidJniObject::callStaticObjectMethod(
                "org/piblaster/piblaster/rfcomm/RfcommClient",
                "rfcommMessage", "(I)Ljava/lang/String;", 0 );
    QAndroidJniObject string2 = QAndroidJniObject::callStaticObjectMethod(
                "org/piblaster/piblaster/rfcomm/RfcommClient",
                "rfcommMessage", "(I)Ljava/lang/String;", 1 );

    _parent->setStatus( string1.toString().toInt() );
    _parent->setStatusMessage( string2.toString() );

     emit gotReply( 0 );


#else

    QThread::msleep( 3000 );
    _parent->setStatusMessage( "XYZ items added to playlist" );
     emit gotReply( 0 );

#endif


}
