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
     */
    Q_INVOKABLE void execCommand( const QString& command );


    /**
     * @brief Call android object to invoke bluetooth connection
     * @return See return codes in RfcommClient.java. Should be 2 for clean connect
     */
    Q_INVOKABLE int connectBluetooth();


    /**
     * @brief Clear send payload buffer. To be used before execCommandWithPayload() and addToSendPayload().
     * Send payload is used for commands with multiple lines like playlist add commands.
     */
    Q_INVOKABLE void clearSendPayload() { _sendPayload.clear(); }


    /**
     * @brief Add a line to send payload. To be used before execCommandWithPayload().
     */
    Q_INVOKABLE void addToSendPayload( const QString& add ) { _sendPayload.append( add ); }

    /**
     * @brief Send command with prepared payload to PyBlaster via bluetooth
     * Fire up new RFCommSendThread to send message.
     * Message will be received by RFCommRecvThread which will emit signal.
     */
    Q_INVOKABLE void execCommandWithPayload( const QString& command );


public slots:
    /**
     * @brief Message buffering slot for incomming messages from RFCommRecvThread
     *
     * This is a dirty hack. We want to send msg object by value from RFCommRecvThread
     * so it may be deleted there (std::map<id,RFCommMessageObject*>), but we
     * need to reemit as pointer to have a clean receive in QML. Don't know, if
     * this is necessary, but it works. Alternative would be use of shared pointers,
     * but seems too complicated.
     *
     * @param msg message object from PI
     */
    void gotMessage( RFCommMessageObject msg );



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

    QList<QString>      _sendPayload;



};

#endif // RFCOMMMASTER_H
