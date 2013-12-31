

import QtQuick 2.0

Rectangle {

    property int index: 0
    property alias text: textItem.text
    color: main.buttonColorActive

    Text {
        id: textItem
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pixelSize: main.baseFontSize
        color: "white"
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            tabClicked(index);
        }
        onPressed: parent.color = main.buttonColorPressed
        onReleased: parent.color = main.buttonColorActive
    }
}
