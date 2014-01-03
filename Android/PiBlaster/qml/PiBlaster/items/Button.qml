

import QtQuick 2.0

Rectangle {

    height: root.buttonHeight
    width: root.buttonWidth
    radius: root.buttonRadius
    color: root.buttonColorActive

    property bool active: true
    property alias text: textItem.text

    function disable() {
        active = false;
        color = root.buttonColorInactive;
        textItem.color = root.buttonColorInactiveText;
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
    }
}
