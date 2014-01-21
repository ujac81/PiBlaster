
#include "Helpers.h"

#include <QThread>



Helpers::Helpers( QObject *parent, QGuiApplication *app )
    : QObject(parent),
    _app( app )
{}


void Helpers::waitLoop()
{
    _waitLoop = 1;

    while ( _waitLoop )
    {
        _app->processEvents();
        QThread::msleep( 10 );
    }
}
