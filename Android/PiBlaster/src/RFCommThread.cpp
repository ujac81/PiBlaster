


#include "RFCommThread.h"

void RFCommThread::run()
{
    QString result = "XYZ items added to playlist";

    QThread::msleep( 3000 );

    emit gotReply( result );
}
