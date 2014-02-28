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
    RFCommSendThread( RFCommMaster* parent, int id, const QString& msg, const QList<QString>& payload = QList<QString>() );

    void run() Q_DECL_OVERRIDE;

signals:
    void commandSent( QString );
    void commBroken( int );
    void gotMessage( RFCommMessageObject );

private:

    RFCommMaster* _parent;
    int _id;
    QString _cmd;
    QList<QString> _payload;    // payload has to be coppied, because master thread might delete it!

};

#endif // RFCOMMSENDTHREAD_H
