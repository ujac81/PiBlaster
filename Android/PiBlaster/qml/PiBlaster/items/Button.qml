

import QtQuick 2.0

Rectangle {

    id: tabBarButton

    property int index: 0
    property alias text: textItem.text
    color: "transparent"

    Text {
        id: textItem
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pixelSize: 20
        color: "white"
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            tabClicked(index);
        }
    }
}
