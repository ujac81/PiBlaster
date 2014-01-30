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


    //////////////////////////// OVERLAYS ////////////////////////////

    // Question dialog if dirs should be added.

    MessageWindow {
        id: noBluetooth
        boxHeight: 400
        caption: "No Bluetooth"
        text: "PiBlaster Remote App was unable to detect bluetooth device or to connect to PyBlaster. Please check and retry connect."
    }

    MessageWindow {
        id: wrongPassword
        boxHeight: 400
        caption: "Wrong Password"
        text: "The PyBlaster daemon did not accept your password. Please set correct password and retry connect"
    }



    //////////////////////////// CENTRAL WINDOW ////////////////////////////


    // buttons column
    Column {
        id: concol
        anchors.centerIn: parent
        spacing: 2 * root.buttonSpacing

        Button {
            id: conButton
            text: "Connect"
            onPressed: connectToPi()
        }

        Button {
            id: disconButton
            text: "Disconnect"
            onPressed: disconnect();
        }
    }

    //////////////////////////// EVENTS ////////////////////////////


    Component.onCompleted: {
        root.status = "Not connected.";
        console.log("Checking BT...");
        rfcomm.checkBluetoothOn();
    }

    // key events
    Keys.onPressed: {
        if (event.key === Qt.Key_Back) {
            event.accepted = true;
            console.log("connect caught back event");
            root.quit();
        }
    }

    //////////////////////////// FUNCTIONS ////////////////////////////

    // called by tab selector upon tab switching to this view.
    function activated() {
        // var status = rfcommClient.connectionStatus;
        // if ( status >= 3 ) {
            conButton.enable();
            disconButton.enable();
//            connected = true;
//        } else {
//            conButton.enable();
//            disconButton.disable();
//            root.status = "Disconnected.";
//            connected = true;
//        }
    }

    /**
     * Call RFCommMaster.connectBluetooth() or raise error message.
     * After sending password, main should receive message with password code
     * and invoke passwordOk() or passwordWrong()
     */
    function connectToPi() {
        if ( rfcomm.connectBluetooth() == 2 ) {
            waitOverlay.caption = "Connecting";
            waitOverlay.text = "Please stand by while connecting to PI...";
            waitOverlay.show();
            rfcomm.execCommand("1234"); // TODO password from settings
        } else {
            noBluetooth.show();
        }
    }

    /// Disconnect from PI, always use this function, don't send 'disconnect' command directly.
    function disconnect() {
        /// @todo check if connected
        waitOverlay.close();
        rfcomm.execCommand('disconnect');
        conButton.enable();
    }

    /// Called by main if password ok code received
    function passwordOk() {
        waitOverlay.close();
        root.status = "Connected.";
    }

    /// Called by main if password ok code received
    function passwordWrong() {
        waitOverlay.close();
        root.status = "Wrong password!";
        wrongPassword.show();
    }

}
