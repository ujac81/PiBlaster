
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
    QString notification() const;

    int tryConnect();

    int connectionStatus();
    int disconnect();
    int disableBT();

    int initAndCountBluetoothMessages();
    QString nextBluetoothMessage() { return m_logentries[m_curlogentry++]; }

signals:
    void notificationChanged();

private slots:
    void updateAndroidNotification();

private:
    QString m_notification;

    QList<QString> m_logentries;    // tempory storage of log entries as list cannot be sent to QML
    int m_curlogentry;              // reset by initAndCountBluetoothMessages(), used by nextBluetoothMessage()
};

#endif // RFCOMMClient_H
