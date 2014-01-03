
#ifndef RFCOMMCLIENT_H
#define RFCOMMCLIENT_H

#include <QObject>
#include <QVariant>
#include <QDebug>

class QAndroidJniObject;

class RFCOMMClient : public QObject
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
    explicit RFCOMMClient(QObject *parent = 0);

    void setNotification(const QString &notification);
    QString notification() const { return m_notification; }

    int tryConnect();

    int connectionStatus();
    int disconnect();
    int disableBT();

    int initAndCountBluetoothMessages();
    QString nextBluetoothMessage() { return m_logentries[m_curlogentry++]; }


    Q_INVOKABLE int execCommand(const QString& command);

    Q_INVOKABLE QString statusMessage() const { return m_statusMessage; }
    Q_INVOKABLE int numResults() const { return m_cmdResult.size(); }
    Q_INVOKABLE QList<QString> result( int i ) const { return m_cmdResultFields[i]; }


signals:
    void notificationChanged();

private slots:
    void updateAndroidNotification();

private:
    QString m_notification;
    int m_status;
    QString m_statusMessage;
    QList<QString> m_cmdResult;
    QList<QList< QString> > m_cmdResultFields;

    QList<QString> m_logentries;    // tempory storage of log entries as list cannot be sent to QML
    int m_curlogentry;              // reset by initAndCountBluetoothMessages(), used by nextBluetoothMessage()
};

#endif // RFCOMMClient_H
