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
            onPressed: connectToPi()
        }

        Button {
            id: disconButton
            text: "Disconnect"
            onPressed: rfcomm.execCommand('disconnect');
        }
    }


    Component.onCompleted: {
        root.status = "Not connected.";

        console.log("Checking BT...");
        rfcomm.checkBluetoothOn();
        console.log("Connect completed.");
    }


    Component.onDestruction: {
        // TODO: disconnect
    }


    function activated() {
        // var status = rfcommClient.connectionStatus;
        // if ( status >= 3 ) {
            conButton.enable();
            disconButton.enable();
            root.status = "Connected.";
//            connected = true;
//        } else {
//            conButton.enable();
//            disconButton.disable();
//            root.status = "Disconnected.";
//            connected = true;
//        }
    }

    function connectToPi() {
        if ( rfcomm.connectBluetooth() == 2 ) {
            rfcomm.execCommand("1234"); // TODO password from settings
//            waitOverlay.caption = "Connecting";
//            waitOverlay.text = "Please stand by while connecting to PI...";
//            waitOverlay.show();
        } else {
            ;

        }
    }

}
