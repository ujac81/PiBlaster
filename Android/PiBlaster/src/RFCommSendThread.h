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
    RFCommSendThread( RFCommMaster* parent, int id, const QString& msg, const QList<QString>& payload );


    void run() Q_DECL_OVERRIDE;


signals:
    void commandSent( QString );
    void commBroken( int );

private:

    RFCommMaster* _parent;
    int _id;
    QString _cmd;
    const QList<QString>& _payload;




};

#endif // RFCOMMSENDTHREAD_H
