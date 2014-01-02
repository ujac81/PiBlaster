
#include <QtGui>
#include <QtQuick>

#include "qtquick2applicationviewer.h"
#include "rfcommclient/rfcommclient.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QtQuick2ApplicationViewer viewer;

    RFCOMMClient *rfcommClient = new RFCOMMClient(&viewer);
    viewer.engine()->rootContext()->setContextProperty(QLatin1String("rfcommClient"),
                                                       rfcommClient);


    viewer.setMainQmlFile(QStringLiteral("qml/PiBlaster/main.qml"));
    viewer.showExpanded();

    return app.exec();
}
