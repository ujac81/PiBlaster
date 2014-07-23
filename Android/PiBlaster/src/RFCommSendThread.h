#ifndef RFCOMMSENDTHREAD_H
#define RFCOMMSENDTHREAD_H


#include <QList>
#include <QString>
#include <QThread>

#include "RFCommMessageObject.h"

class RFCommMaster;

class RFCommSendThread : public QThread
{
Q_OBJECT

public:
    RFCommSendThread( RFCommMaster* parent, int id, const QString& msg,
                      const QList<QString>& payload = QList<QString>() );

    void run() Q_DECL_OVERRIDE;

    /**
     * True if this thread is finished
     * Also true if send failed and thread may be killed.
     */
    bool sendDone() const { return _sendDone; }

signals:
    void commandSent( QString );
    void commBroken( int );
    void gotMessage( RFCommMessageObject );

private:

    RFCommMaster* _parent;
    int _id;
    QString _cmd;

    // payload has to be coppied, because master thread might delete it!
    QList<QString> _payload;

    // true if this thread may be closed
    bool _sendDone;
};

#endif // RFCOMMSENDTHREAD_H
