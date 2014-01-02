

#include "rfcommclient.h"
#include <QtDebug>

RFCOMMClient::RFCOMMClient(QObject *parent)
    : QObject(parent)
{
    connect(this, SIGNAL(notificationChanged()), this, SLOT(updateAndroidNotification()));

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
}


int RFCOMMClient::tryConnect()
{
    return 3;
}

int RFCOMMClient::disconnect()
{
    return 0;
}

int RFCOMMClient::disableBT()
{
    return 0;
}

int RFCOMMClient::connectionStatus()
{
    return 3;
}


int RFCOMMClient::initAndCountBluetoothMessages()
{
    m_logentries.clear();
    m_logentries.append("Some funny");
    m_logentries.append("bluetooth messages");
    m_logentries.append("in here");


    m_curlogentry = 0;
    return m_logentries.size();
}

