import QtQuick 2.0


Item {
    id: dialogComponent
    anchors.fill: parent
    property int retval: -1

    PropertyAnimation { target: dialogComponent; property: "opacity";
                                  duration: 400; from: 0; to: 1;
                                  easing.type: Easing.InOutQuad ; running: true }

    Rectangle {
        anchors.fill: parent
        id: overlay
        color: "#000000"
        opacity: 0.6
        MouseArea { anchors.fill: parent }
    }

    Rectangle {
        id: dialogWindow
        width: 100
        height: 62
        radius: 10
        anchors.centerIn: parent

        Text {
            anchors.centerIn: parent
            text: "This is the popup"
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                retval = 1;
                rfcommClient.wait = 0;
            }
        }
    }

    Component.onCompleted: {
        console.log("Dialog ready!");

    }

    function wait() {
        rfcommClientz.waitLoop();
    }
}
