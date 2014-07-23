import QtQuick 2.0

import "../items"

/**
 * Connect view -- display (dis)connect buttons
 *
 */
Item {
    id: connectOverlay
    z: 111

    // do not define parent to fill complete window
    anchors.fill: parent
    visible: connectOverlay.opacity !== 0
    // show() will raise opacity
    opacity: 0

    // Fill complete area with MouseArea to catch touch events
    Rectangle {
        anchors.fill: parent
        id: overlay
        color: "#000000"
        opacity: 0.6
        MouseArea { anchors.fill: parent }
    }


    Button {
        id: conButton
        text: "Connect"
        onPressed: connectToPi()
        anchors.centerIn: parent
    }

    //////////////////////////// OVERLAYS ////////////////////////////

    WaitOverlay {
        id: noBluetoothOver
        z: 112
        caption: "Bluetooth"
        text: "No bluetooth device has been detected. Please enable bluetooth
at application start. Press back key to leave application."
    }

    WaitOverlay {
        id: connectOver
        z: 112
        caption: "Connecting"
        text: "Please stand by while connecting."
    }

    WaitOverlay {
        id: wrongPWOver
        z: 112
        caption: "Password"
        text: "Password has not been accepted by PiBlaster. Please set
correct password in settings."
    }





    //////////////////////////// EVENTS ////////////////////////////

    Component.onCompleted: {
        root.status = "Not connected.";
        console.log("Checking BT...");
        rfcomm.checkBluetoothOn();
        show();
    }

    //////////////////////////// TRIGGERS ////////////////////////////

    /**
     * just quit if back key pressed in not connected mode
     */
    function handleBackKey() {
        root.quit();
    }

    //////////////////////////// FUNCTIONS ////////////////////////////


    /**
     * Call RFCommMaster.connectBluetooth() or raise error message.
     * After sending password, main should receive message with password code
     * and invoke passwordOk() or passwordWrong()
     */
    function connectToPi() {
        if ( rfcomm.connectBluetooth() == 2 ) {
            connectOver.show();
            rfcomm.execCommand("1234"); // TODO password from settings
        } else {
            noBluetoothOver.show();
        }
    }

    /// Disconnect from PI, always use this function,
    /// don't send 'disconnect' command directly.
    function disconnect() {
        /// @todo check if connected
        console.log("invoking disconnect...");
        rfcomm.execCommand('disconnect');
        show();
    }

    /// Called by main if password ok code received
    function passwordOk() {
        root.status = "Connected.";
        close();
    }

    /// Called by main if password ok code received
    function passwordWrong() {
        root.status = "Wrong password!";
        wrongPWOver.show();
    }

    // animate opacity, 250ms to raise/fall
    Behavior on opacity {
        NumberAnimation { duration: 250 }
    }

    // close and hide window
    function close() {
        connectOver.close();
        opacity = 0;
    }

    // invoke from outside to raise message
    function show() {
        opacity = 1;
        wrongPWOver.close();
    }

}
