
#ifndef RFCOMMCLIENT_H
#define RFCOMMCLIENT_H

#include <QQmlEngine>
#include <QGuiApplication>
#include <QObject>
#include <QVariant>
#include <QDebug>
#include <qqml.h>

class QAndroidJniObject;

/**
 * @brief QML to JAVA interface for bluetooth-communication to PyBlaster
 */
class RFCommClient : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString notification READ notification WRITE setNotification NOTIFY notificationChanged)
    Q_PROPERTY(int tryConnect READ tryConnect)
    Q_PROPERTY(int initAndCountBluetoothMessages READ initAndCountBluetoothMessages)
    Q_PROPERTY(QString nextBluetoothMessage READ nextBluetoothMessage)
    Q_PROPERTY(int connectionStatus READ connectionStatus)
    Q_PROPERTY(int disconnect READ disconnect)
    Q_PROPERTY(int disableBT READ disableBT)

public:

    /**
     * @brief Init QObject and set some signals
     * @param parent viewer object
     * @param app pointer to GUI event queue
     */
    explicit RFCommClient( QObject *parent = 0, QGuiApplication* app = 0 );

    /// @brief Getter/Setter for android notification
    void setNotification( const QString &notification );
    QString notification() const { return _notification; }


    /**
     * @brief Call android object to invoke bluetooth connection
     * @return See return codes in RfcommClient.java. Should be 3 for clean connect
     */
    int tryConnect();

    /**
     * @brief Read android bluetooth connection status
     * @return See return codes in RfcommClient.java. Should be 3 for clean connect
     */
    int connectionStatus();

    /**
     * @brief Disconnect bluetooth
     * @return Should return 0 on clean disconnect
     */
    int disconnect();

    /**
     * @brief Try to disable bluetooth -- not functional atm.
     * @return 0 if disabled ok
     */
    int disableBT();

    /**
     * @brief Prepare read out of bluetooth log messages from java interface
     *
     * Use this function before calling nextBluetoothMessage() N times, where
     * N is return value of this function.
     * This is a dirty iterator-like approach to parse QStringList from QML
     *
     * @return number of rows in bluetooth message stack
     */
    int initAndCountBluetoothMessages();
    /**
     * @brief Get next bluetooth message from buffer
     * call N = initAndCountBluetoothMessages() before and call this<
     * function N times.
     */
    QString nextBluetoothMessage() { return _logentries[_curlogentry++]; }


    /**
     * @brief Send plain command to PyBlaster via bluetooth
     * @return return value as received by PyBlaster. See evalcmd.py for codes, 0 means ok.
     */
    Q_INVOKABLE int execCommand(const QString& command);

    /**
     * @brief Get status message received with last command executed on PyBlaster
     * @return short status message from PyBlaster
     */
    Q_INVOKABLE QString statusMessage() const { return _statusMessage; }

    /// @brief set last bluetooth message from external (e.g. RFCommThread)
    void setStatusMessage( const QString& msg ) { _statusMessage = msg; }

    /// @brief set last bluetooth status from external (e.g. RFCommThread)
    void setStatus(int status) { _status = status; }


    /**
     * @brief Number of payload rows received with last execCommand() call from PyBlaster
     * @return number of rows in result()
     */
    Q_INVOKABLE int numResults() const { return _cmdResult.size(); }
    /// @brief payload result row received from PyBlaster
    Q_INVOKABLE QList<QString> result( int i ) const { return _cmdResultFields[i]; }

    /**
     * @brief Clear mass send buffer to send multiple playlist modification calls in a row
     * @param mode Playlist add mode (0=append, 1=insert, 2=random)
     */
    Q_INVOKABLE void preparePlaylistAdd( int mode );
    /**
     * @brief Push playlist add item to mass send buffer
     */
    Q_INVOKABLE void addPlaylistItem( const QString& row );

    /**
     * @brief Perform (threaded) mass send operation via RFCommThread
     * Will emit signal addToPlaylistFinished() after finished.
     * Read statusMessage() after signal received.
     * @return 0 if ok (connected)
     */
    Q_INVOKABLE int sendPlaylistAdd();


    /// @brief playlist add instructions accessor for RFCommThread
    const QList<QString>& playlistAddItems() const { return _plAddList; }

    /// @brief playlist add mode accessor for RFCommThread
    int playlistAddMode() const { return _plAddMode; }


signals:
    void notificationChanged();
    void addToPlaylistFinished(int);

private slots:
    void updateAndroidNotification();

private:

    QGuiApplication*            _app;               ///< Qt event loop accessor

    QString                     _notification;      ///< android notification buffer
    int                         _status;            ///< status code of last command sent to PyBlaster
    QString                     _statusMessage;     ///< status msg received with last command sent to PyBlaster
    QList<QString>              _cmdResult;         ///< result rows of last command senT to PyBlaster
    QList<QList< QString> >     _cmdResultFields;   ///< tokkens of rows of _cmdResult
    QList<QString>              _plAddList;         ///< command buffer for playlist add instructions
    int                         _plAddMode;         ///< mode buffer for playlist add instructions (append/insert/random/...)

    QList<QString>              _logentries;        ///< tempory storage of log entries as list cannot be sent to QML
    int                         _curlogentry;       ///< reset by initAndCountBluetoothMessages(), used by nextBluetoothMessage()
};

QML_DECLARE_TYPEINFO(RFCommClient, QML_HAS_ATTACHED_PROPERTIES)

#endif // RFCOMMClient_H
