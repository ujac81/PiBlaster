

import QtQuick 2.0

Rectangle {

    signal pressed


    height: root.buttonHeight
    width: root.buttonWidth
    radius: root.buttonRadius
    color: root.buttonColorActive
    border.width: 2
    border.color:  root.colorButtonBoxFrame

    property bool active: true
    property alias text: textItem.text

    function disable() {
        active = false;
        color = root.buttonColorInactive;
        textItem.color = root.buttonColorInactiveText;
        border.color =  root.buttonColorInactiveText;
    }
    function enable() {
        active = true;
        color = root.buttonColorActive;
        textItem.color = root.buttonColorActiveText;
    }

    Text {
        id: textItem
        anchors.centerIn: parent
        color: root.buttonColorActiveText
        font.pixelSize: root.baseFontSize
    }

    MouseArea {
        id: mousearea
        signal pushed
        anchors.fill: parent
        onClicked: {
            if ( active ) pushed()
        }
        onPressed: { if ( active ) { color = root.buttonColorPressed; } }
        onReleased: { if ( active ) { color = root.buttonColorActive; } }
    }

    Component.onCompleted: {
          mousearea.clicked.connect(pressed)
    }

}
