import QtQuick 2.0

import "../items"

/**
 * Connect view -- display (dis)connect buttons
 *
 */
Rectangle {
    id: connect
    anchors.fill: parent
    color: "transparent"

    property bool connected: false

    // buttons column
    Column {
        id: concol
        anchors.centerIn: parent
        spacing: root.buttonSpacing

        Button {
            id: conButton
            text: "Connect"

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if ( parent.active ) {
                        parent.color = root.buttonColorPressed;
                        var constat = rfcommClient.tryConnect
                        root.status = "Connected: " + constat
                        parent.color = root.buttonColorActive;
                        connect.activated()
                    }
                }
                onPressed: { if ( parent.active ) { parent.color = root.buttonColorPressed; } }
                onReleased: { if ( parent.active ) { parent.color = root.buttonColorActive; } }
            }
        }
        Button {
            id: disconButton
            text: "Disconnect"

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if ( parent.active ) {
                        var constat = rfcommClient.disconnect;
                        connect.activated()
                    }
                }
                onPressed: { if ( parent.active ) { parent.color = root.buttonColorPressed; } }
                onReleased: { if ( parent.active ) { parent.color = root.buttonColorActive; } }
            }
        }
    }


    Component.onCompleted:
    {
        root.status = "Not connected."
        console.log("Connect.qml start")
    }

    Component.onDestruction:
    {
        console.log("Connect.qml quit")
    }

    function activated()
    {
        var status = rfcommClient.connectionStatus;
        if ( status >= 3 ) {
            conButton.disable();
            disconButton.enable();
            root.status = "Connected.";
            connected = true;
        } else {
            conButton.enable();
            disconButton.disable();
            root.status = "Disconnected.";
            connected = true;
        }
    }
}
