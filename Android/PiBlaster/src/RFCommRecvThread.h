#ifndef RFCOMMRECVTHREAD_H
#define RFCOMMRECVTHREAD_H

#include <map>

#include <QThread>

#include "RFCommMessageObject.h"

class RFCommMaster;

class RFCommRecvThread : public QThread
{
Q_OBJECT

public:

    /// 30ms polling time in wait loop
    static const int PollTime = 30;

    RFCommRecvThread( RFCommMaster* parent );
    ~RFCommRecvThread();

    void run() Q_DECL_OVERRIDE;


public slots:
    void abort();


signals:
    void gotMessage( RFCommMessageObject );
    void commBroken( int );
    void bluetoothMessage( QString );

private:

    RFCommMessageObject* newMessageObject( int id, int status, int code,
                                           int plSize, const QString& msg );

    void messageDone( int id, RFCommMessageObject* );


    RFCommMaster*                           _parent;

    bool                                    _run;

    std::map<int, RFCommMessageObject*>     _recvBuffer;


};

#endif // RFCOMMRECVTHREAD_H
