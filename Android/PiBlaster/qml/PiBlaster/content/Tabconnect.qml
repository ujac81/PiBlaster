import QtQuick 2.0

Rectangle {
    anchors.fill: parent
    color: "transparent"


    Text {
        anchors.centerIn: parent
        text: "connect"

        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (rfcommClient.hasBluetooth == -1)
                    parent.text = "no bluetooth adapter"
                else if (rfcommClient.hasBluetooth == -2)
                    parent.text = "bluetooth disabled"
                else if (rfcommClient.hasBluetooth == 0)
                    parent.text = "bluetooth ok"
                else
                    parent.text = "bluetooth unkown"
            }
            onPressed: parent.scale = 1.2
            onReleased: parent.scale = 1.0
        }
    }
}
