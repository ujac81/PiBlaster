import QtQuick 2.0



Item {
    id: waitOverlay
    z: 110

    // do not define parent to fill complete window
    anchors.fill: parent
    visible: waitOverlay.opacity !== 0
    // show() will raise opacity
    opacity: 0

    property alias caption: caption.text
    property alias text: messageText.text

    property int boxWidth: 300
    property int boxHeight: 300


    MessageWindow {
        id: breakWaitAndExit
        boxHeight: 400
        z: 120
        caption: "Exit application"
        text: "App is in wait mode. Stop waiting and leave?"
        onAccepted: root.quit();

        // This is not nice, but will give a chance to hide wait overlay
        // if it's deadlocking.
        onCanceled: parent.close();
    }



    // Fill complete area with MouseArea to catch touch events
    Rectangle {
        anchors.fill: parent
        id: overlay
        color: "#000000"
        opacity: 0.6
        MouseArea { anchors.fill: parent }
    }

    // central button box including caption and text
    ButtonBox {
        id: messageBox
        anchors.centerIn: parent
        width: waitOverlay.boxWidth
        height: waitOverlay.boxHeight

        // box caption
        Rectangle {
            id: header
            width: parent.width
            anchors.top: parent.top

            height: root.buttonHeight
            radius: 10
            border.width: 4
            border.color:  root.colorButtonBoxFrame
            color: "white"

            // caption text
            Text {
                id: caption
                anchors.centerIn: parent
                anchors.rightMargin: root.buttonHeight + 5
                color: root.buttonColorActiveText
                font.pixelSize: root.baseFontSize
                text: "CAPTION"
            }
        }

        // lower colum, include text and button row
        Column {

            anchors.centerIn: parent
            anchors.top: header.bottom
            width: parent.width - 2 * root.buttonSpacing
            spacing: root.buttonSpacing

            Text {
                id: messageText
                text: "QUESTION"
                width: parent.width
                wrapMode: Text.Wrap
                font.pixelSize: root.baseFontSize
            }

        }
    }

    // animate opacity, 250ms to raise/fall
    Behavior on opacity {
        NumberAnimation { duration: 250 }
    }

    // close and hide window
    function close() {
        waitOverlay.opacity = 0
        waitOverlay.focus = false;
    }

    // invoke from outside to raise message
    function show() {
        waitOverlay.opacity = 1
        waitOverlay.focus = true;
    }

    // If wait overlay is active and back key was pressed, ask to quit
    function handleBackKey() {
        if ( waitOverlay.opacity != 0 ) {
            console.log("wait overlay caught back event");
            breakWaitAndExit.show();
            return true;
        }
        return false;
    }
}
