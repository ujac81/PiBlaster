
#ifndef RFCOMMCLIENT_H
#define RFCOMMCLIENT_H

#include <QQmlEngine>
#include <QGuiApplication>
#include <QObject>
#include <QVariant>
#include <QDebug>
#include <qqml.h>

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
    explicit RFCOMMClient(QObject *parent = 0, QGuiApplication* app = 0);

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

    Q_INVOKABLE void preparePlaylistAdd( int mode );
    Q_INVOKABLE void addPlaylistItem( const QString& row );

    Q_INVOKABLE int sendPlaylistAdd();


signals:
    void notificationChanged();
    void addToPlaylistFinished(const QString& );

private slots:
    void updateAndroidNotification();

private:

    QGuiApplication* m_app;


    QString m_notification;
    int m_status;
    QString m_statusMessage;
    QList<QString> m_cmdResult;
    QList<QList< QString> > m_cmdResultFields;
    QList<QString> _plAddList;
    int _plAddMode;

    QList<QString> m_logentries;    // tempory storage of log entries as list cannot be sent to QML
    int m_curlogentry;              // reset by initAndCountBluetoothMessages(), used by nextBluetoothMessage()
};

QML_DECLARE_TYPEINFO(RFCOMMClient, QML_HAS_ATTACHED_PROPERTIES)

#endif // RFCOMMClient_H
