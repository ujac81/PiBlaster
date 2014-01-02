

#include "rfcommclient.h"

#include <QtAndroidExtras/QAndroidJniObject>
#include <QtDebug>

RFCOMMClient::RFCOMMClient(QObject *parent)
    : QObject(parent)
{
    connect(this, SIGNAL(notificationChanged()), this, SLOT(updateAndroidNotification()));

    m_rfcomm = new QAndroidJniObject("org/piblaster/piblaster/rfcomm/RfcommClient");

    qDebug() << "Started RFCOMMClient... m_rfcomm = " << m_rfcomm << ", has bluetooth = " << hasBluetooth();

    m_rfcomm->callMethod<void>("requestBluetooth");

    setNotification("Started...");

}

void RFCOMMClient::setNotification(const QString &notification)
{
    if (m_notification == notification)
        return;

    qDebug() << "setNotification: " << notification;

    m_notification = notification;
    emit notificationChanged();
}

QString RFCOMMClient::notification() const
{
    return m_notification;
}

void RFCOMMClient::updateAndroidNotification()
{
    qDebug() << "updateNotification: " << m_notification;

    QAndroidJniObject javaNotification = QAndroidJniObject::fromString(m_notification);
    m_rfcomm->callMethod<void>("notify", "(Ljava/lang/String;)V",
                               javaNotification.object<jstring>());

}


int RFCOMMClient::hasBluetooth()
{
    m_rfcomm->callMethod<void>("testBluetooth");
    jint res = m_rfcomm->callMethod<jint>("hasBluetooth");
    qDebug() << "check bluetooth: " << res;
    return res;
}

