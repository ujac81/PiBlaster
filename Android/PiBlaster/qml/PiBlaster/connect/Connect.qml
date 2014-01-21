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

            onPressed: {
                var constat = rfcommClient.tryConnect
                connect.activated();
            }
        }

        Button {
            id: disconButton
            text: "Disconnect"

            onPressed: {
                var constat = rfcommClient.disconnect;
                connect.activated();
            }
        }
    }


    Component.onCompleted: {
        root.status = "Not connected."
    }

    Component.onDestruction: {
        // TODO: disconnect
    }

    function activated() {
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
