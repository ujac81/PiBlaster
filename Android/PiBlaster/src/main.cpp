
#include <QtGui>
#include <QtQuick>

#include "QtQuick2ApplicationViewer.h"

#include "RFCommMaster.h"
#include "RFCommMessageObject.h"

#include <QMetaType>
#include <QtDebug>

int main(int argc, char *argv[])
{

    qDebug() << "==== 1 ====";

    QGuiApplication app(argc, argv);
    qRegisterMetaType<RFCommMessageObject>( "RFCommMessageObject" );

    qDebug() << "==== 2 ====";

    QtQuick2ApplicationViewer viewer;

    qDebug() << "==== 3 ====";

    RFCommMaster* rfcomm = new RFCommMaster( &viewer );

    qDebug() << "==== 4 ====";

    viewer.engine()->rootContext()->setContextProperty( "rfcomm", rfcomm );

    qDebug() << "==== 5 ====";

    viewer.setSource(QUrl("qrc:/qml/PiBlaster/main.qml"));
    viewer.showExpanded();

    qDebug() << "==== 6 ====";

    return app.exec();

    qDebug() << "==== END ====";
}
