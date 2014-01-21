


#include "RFCommThread.h"

void RFCommThread::run() Q_DECL_OVERRIDE
{
    QString result = "msg";

    QThread::msleep( 4000 );

    emit gotReply( result );
}
