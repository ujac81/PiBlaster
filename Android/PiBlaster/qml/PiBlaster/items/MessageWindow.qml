import QtQuick 2.0


/**
 * @brief Place question dialog on top layer
 *
 * Emits
 * - accepted if OK button pressed
 * - rejected if Cancel button pressed
 * - canceled if X pressed
 *
 * Use show() to raise MessageWindow
 */
Item {

    z: 100
    id: container

    // do not define parent to fill complete window
    anchors.fill: container.fill ? parent : undefined
    visible: container.opacity !== 0
    // show() will raise opacity
    opacity: 0

    property bool fill: true
    property alias caption: caption.text
    property alias text: questionText.text
    property int boxWidth: 300
    property int boxHeight: 300

    signal accepted
    signal rejected
    signal canceled

    // Fill complete area with MouseArea to catch touch events
    Rectangle {
        anchors.fill: parent
        id: overlay
        color: "#000000"
        opacity: 0.6
        MouseArea { anchors.fill: parent }
    }

    // central button box including caption, text and OK|Cancel buttons
    ButtonBox {
        id: messageBox
        anchors.centerIn: parent
        width: container.boxWidth
        height: container.boxHeight

        // box caption with X-button
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

            // X-button -> cancel if pressed
            Rectangle {
                height: root.buttonHeight
                width: root.buttonHeight * 1.5
                anchors.right: parent.right
                anchors.top: parent.top

                radius: 10
                border.width: 4
                border.color:  root.colorButtonBoxFrame
                color: root.buttonColorInactive

                Image {
                    anchors.centerIn: parent
                    width: root.buttonHeight - 15
                    height: root.buttonHeight - 15
                    source: "qrc:///images/images/x-nopad.png"
                }
                MouseArea {
                    anchors.fill: parent
                    onPressed: close(-1)
                }
            }
        }

        // lower colum, include text and button row
        Column {

            anchors.centerIn: parent
            anchors.top: header.bottom
            width: parent.width - 2 * root.buttonSpacing
            spacing: root.buttonSpacing

            Text {
                id: questionText
                text: "QUESTION"
                width: parent.width
                wrapMode: Text.Wrap
                font.pixelSize: root.baseFontSize
            }

            Row {
                width: parent.width
                x: root.buttonSpacing
                spacing: root.buttonSpacing

                Button {
                    id: yesButton
                    text: "OK"
                    width: ( parent.width - 3 * root.buttonSpacing ) / 2
                    onPressed: close(1)
                }
                Button {
                    id: noButton
                    text: "Cancel"
                    width: ( parent.width - 3 * root.buttonSpacing ) / 2
                    onPressed: close(0)
                }
            }
        }
    }

    // animate opacity, 250ms to raise/fall
    Behavior on opacity {
        NumberAnimation { duration: 250 }
    }


    // emit signals on close and hide window
    function close(retval) {
        if (retval == -1) canceled();
        if (retval == 1) accepted();
        if (retval == 0) rejected();
        container.opacity = 0
    }


    // invoke from outside to raise dialog
    function show() {
        container.opacity = 1
    }
}

