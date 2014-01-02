
#ifndef RFCOMMCLIENT_H
#define RFCOMMCLIENT_H

#include <QObject>

class QAndroidJniObject;

class RFCOMMClient : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString notification READ notification WRITE setNotification NOTIFY notificationChanged)
    Q_PROPERTY(bool hasBluetooth READ hasBluetooth)

public:
    explicit RFCOMMClient(QObject *parent = 0);

    void setNotification(const QString &notification);
    QString notification() const;

    int hasBluetooth();

signals:
    void notificationChanged();

private slots:
    void updateAndroidNotification();

private:
    QString m_notification;


    QAndroidJniObject* m_rfcomm;
};

#endif // RFCOMMClient_H
