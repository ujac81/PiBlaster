import QtQuick 2.0

Rectangle {

    property alias text: textEdit.text

    signal enterPressed;
    signal cleared;

    width: 300
    height: 40
    radius: 10
    border.width: 4
    border.color: "black"
    color: "transparent"
    focus: true

    TextInput {
        id: textEdit
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 60
        anchors.bottomMargin: 8
        anchors.topMargin: 8
        clip: false
        maximumLength: 25
        cursorVisible: false

        text: "quick filter"
        font.pixelSize: parent.height - 16

        function clear() {
            text = ""
            parent.cleared();
        }

        onFocusChanged: {
            console.log("focus change: "+focus);
            if ( focus) clear();
        }

        Keys.onPressed: {
            if (event.key == Qt.Key_Return || event.key == Qt.Key_Return) {
                Qt.inputMethod.hide();
                cursorVisible = false;
                parent.enterPressed();
            }
        }
    }

    Rectangle {
        width: 50
        height: parent.height - 12
        x: parent.width - 50 - 6
        y: 6
        radius: 6
        color: "#39393908"
        Image {
            anchors.centerIn: parent
            width: parent.height - 4
            height: parent.height - 4
            source: "qrc:///images/images/x-nopad.png"

        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                textEdit.clear()
            }
        }
    }
}
