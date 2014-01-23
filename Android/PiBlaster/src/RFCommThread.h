#ifndef RFCOMMTHREAD_H
#define RFCOMMTHREAD_H

#include <QThread>

class RFCommClient;

class RFCommThread : public QThread
{
Q_OBJECT

public:

    RFCommThread( RFCommClient* parent );

    void run() Q_DECL_OVERRIDE;


signals:
    void gotReply( int );

private:

    RFCommClient* _parent;


};

#endif // RFCOMMTHREAD_H
