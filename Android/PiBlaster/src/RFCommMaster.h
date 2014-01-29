#ifndef RFCOMMMASTER_H
#define RFCOMMMASTER_H

#include <QQmlEngine>
#include <QGuiApplication>
#include <QObject>
#include <QVariant>
#include <QDebug>
#include <qqml.h>

#include <RFCommMessageObject.h>

class QAndroidJniObject;
class RFCommRecvThread;

class RFCommMaster : public QObject
{
    Q_OBJECT
public:

    /**
     * @brief Init QObject and set some signals
     * @param parent viewer object
     * @param app pointer to GUI event queue
     */
    explicit RFCommMaster( QObject* parent = 0 );

    /**
     * @brief delete send thread?
     * @TODO maybe done by QT?
     */
    ~RFCommMaster();

    /**
     * @brief Check if bluetooth is on, request turn on otherwise.
     * Emits bluetoothOff() if bluetooth is not on
     */
    Q_INVOKABLE void checkBluetoothOn();


    /**
     * @brief Call state of bluetooth connection.
     * Emit signal after call. May be called from multiple places
     */
    Q_INVOKABLE void callBluetoothState();

    /**
     * @brief Send plain command to PyBlaster via bluetooth
     * Fire up new RFCommSendThread to send message.
     * Message will be received by RFCommRecvThread which will emit signal
     * @return return 1 if send ok (comm not broken)
     */
    Q_INVOKABLE void execCommand( const QString& command );


    /**
     * @brief Call android object to invoke bluetooth connection
     * @return See return codes in RfcommClient.java. Should be 2 for clean connect
     */
    Q_INVOKABLE int connectBluetooth();


public slots:
    void gotMessage( RFCommMessageObject msg )
    {
       qDebug()  << " ==== YEAH got it ==== ";
       emit receivedMessage( &msg );
    }



signals:
    void bluetoothState( int );
    void commandSent( QString );
    void commBroken( int );
    void receivedMessage( RFCommMessageObject* );
    void bluetoothMessage( QString );

private:
    void generateReceiveThread();

    RFCommRecvThread*   _recv;
    int                 _msgId;



};

#endif // RFCOMMMASTER_H
