#ifndef RFCOMMTHREAD_H
#define RFCOMMTHREAD_H

#include <QThread>

class RFCommThread : public QThread
{
Q_OBJECT

public:

    RFCommThread( QObject* parent ) : QThread( parent ) {}

    void run();


signals:
    void gotReply( const QString& );


};

#endif // RFCOMMTHREAD_H
