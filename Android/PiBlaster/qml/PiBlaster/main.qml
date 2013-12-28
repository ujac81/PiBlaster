import QtQuick 2.0
import "content"

// main rectangular for full App
// mainWidth and mainHeight will be set from external
Rectangle {
    property int mainWidth: 320
    property int mainHeight: 480

    id: main
    width: mainWidth
    height: mainHeight
    focus: true

    // background color gradient -- all rectangles should be transparent
    gradient: Gradient {
        GradientStop { position: 0; color: "#94d9ff" }
        GradientStop { position: 1; color: "#67B3FF" }
    }

    // header caption
    Text {
        id: caption
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 35
        text: "PiBlaster Remote"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pixelSize: 25
    }

    // tabbbed UI holding main tab bars and controls
    Tabview {
        id: tabview

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: caption.bottom
        anchors.bottom: parent.bottom
    }
}
