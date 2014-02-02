
import QtQuick 2.0

import "tabview"
import "items"

/**
 * Root for full App
 *
 * -- definition of constants
 * -- creates TabView
 * -- handles global key events
 */
Rectangle {
    id: root

    property int mainWidth: 540   // default for testing, will be changed upon start
    property int mainHeight: 800  // default for testing, will be changed upon start


    ///// application constants /////

    property string versionInfo: "0.2.1"

    property string color1: "#94d9ff"   // upper background gradient color
    property string color2: "#67B3FF"   // lower background gradient color
    property int statusbarHeight: 20    // lower status bar
    property int barHeight: 36          // tab bar
    property int baseFontSize: 24       // standard font pixel size
    property int buttonHeight: 40       // default height for pop-up buttons1
    property int buttonWidth: 220       // default width for pop-up buttons1
    property int buttonRadius: 5        // corner radius for button
    property int buttonSpacing: 20      // spacing between multiple buttons
    property string buttonColorActive: "#1855FF"            // clickable button color
    property string buttonColorPressed: "#1212FF"           // pressed down (active) button color
    property string buttonColorActiveText: "black"          // active button text color
    property string buttonColorInactive: "#8B8E91"          // greyed out button color
    property string buttonColorInactiveText: "#5C5E60"      // greyed out button text color
    property string colorSelected: "#1212FF"                // background color for selected items in lists
    property string colorUnselected: "#dddddd"          // background color for odd-indexed items in lists
    property string colorUnselected2: "#bbbbbb"             // background color for even-indexed items in lists
    property string colorButtonBox:         "#2382FF"
    property string colorButtonBoxFrame:    buttonColorPressed

    property alias status: status.text
    property alias tabview: tabview

    width: mainWidth
    height: mainHeight
    focus: true

    MessageWindow {
        id: messageWindow
        visible: false
    }


    // background color gradient -- all rectangles should be transparent
    gradient: Gradient {
        GradientStop { position: 0; color: root.color1 }
        GradientStop { position: 1; color: root.color2 }
    }

    // header caption
    Text {
        id: caption
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 35
        text: "PiBlaster Remote v" + versionInfo
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pixelSize: 25
    }

    // lower status bar for short info messages
    Rectangle {
        id: statusBar
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: root.statusbarHeight
        color: "black"

        Text {
            id: status
            anchors.fill: parent
            color: "white"
            text: "PiBlaster Remote started"
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: root.statusbarHeight - 5
        }
    }

    // tabbbed UI holding main tab bars and controls
    TabView {
        id: tabview
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: caption.bottom
        anchors.bottom: statusBar.top
    }


    Component.onCompleted: {

        // emitted by RFCommSendThread if send to BT socket ok
        rfcomm.commandSent.connect(messageSent);

        // emitted by RFCommSendThread if send to BT socket not ok
        // emitted by RFCommRecvThread if socket broken
        rfcomm.commBroken.connect(commBroken);

        // emitted by RFCommMaster after checking bluetooth
        rfcomm.bluetoothState.connect(bluetoothState);

        // emitted by RFCommMaster after checking bluetooth
        rfcomm.bluetoothMessage.connect(bluetoothMessage);

        // emitted by RFCommRecvThread for each incomming message
        rfcomm.receivedMessage.connect(messageRecvd);

        console.log("main completed.");
    }



    ////////////////// OVERLAYS //////////////////

    WaitOverlay {
        id: waitOverlay
        parent: root
    }

    MessageWindow {
        id: quitQuestion
        boxHeight: 300
        caption: "Leave Application"
        text: "Do you want to exit PiBlaster Remote App?"
        onAccepted: root.quit();
    }


    ////////////////// COMMUNICATION //////////////////

    function messageSent(code) {
        console.log("Message has been sent "+code);
    }

    function commBroken(code) {
        console.log("RFComm broken -- code "+code);
    }

    function bluetoothState(code) {
        console.log("Bluetooth state changed -- code "+code);
    }

    function bluetoothMessage(msg) {
        console.log("Bluetooth msg: "+msg);
    }

    function messageRecvd(msg) {
        console.log("Got message: id="+msg.id()+", status="+msg.status()+", code="+msg.code()+
                    ", payload_size="+msg.payloadSize()+", msg="+msg.message());

        if ( msg.code() == 1 ) {
            tabview.tabsModel.children[3].passwordOk();
        } else if ( msg.code() == 2 ) {
            tabview.tabsModel.children[3].passwordWrong();
        } else if ( msg.code() == 101 ) {
            tabview.tabsModel.children[1].received_showdev_data(msg);
        } else if ( msg.code() == 102 ) {
            tabview.tabsModel.children[1].received_dir_data(msg);
        }
    }


    function connected() {
        /// @todo check
        return true;
    }


    /**
     * Called on serious errors and if back pressed in main menu.
     * Tries to disconnect bluetooth.
     */
    function quit() {
        console.log("leaving...");
        tabview.tabsModel.children[3].disconnect();
        Qt.quit();
    }

    function log_error(msg) {
        /// @todo add to log
        // status = msg;
    }


    /**
     * Back key handling in QML does not work properly.
     * Back key is handled in the C++ part which calls this
     * function if back key is released.
     */
    function handleBackPressed()
    {
        console.log("handleBackPressed caught back button");

        // ask wait overlay 1st to catch back key
        if ( ! waitOverlay.handleBackKey() )
            // if active tab returns true, it used the back event
            if ( ! tabview.currentTab().handleBackKey() )
                // back event was unused -- ask to quit
                quitQuestion.show();
    }


}
