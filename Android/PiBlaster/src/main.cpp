
#include <QtGui>
#include <QtQuick>

#include "QtQuick2ApplicationViewer.h"

#include "RFCommClient.h"
#include "Helpers.h"

#include <QtDebug>

int main(int argc, char *argv[])
{

    qDebug() << "==== 1 ====";

    QGuiApplication app(argc, argv);

    qDebug() << "==== 2 ====";

    QtQuick2ApplicationViewer viewer;

    qDebug() << "==== 3 ====";

    RFCOMMClient* rfcommClient = new RFCOMMClient( &viewer, &app );
    Helpers* helpers = new Helpers( &viewer, &app );

    qDebug() << "==== 4 ====";

    viewer.engine()->rootContext()->
            setContextProperty( "rfcommClient", rfcommClient );

    viewer.engine()->rootContext()->
            setContextProperty( "helpers", helpers );

    qDebug() << "==== 5 ====";


    viewer.setMainQmlFile(QStringLiteral("qml/PiBlaster/main.qml"));
    viewer.showExpanded();

    qDebug() << "==== 6 ====";

    return app.exec();

    qDebug() << "==== END ====";
}
