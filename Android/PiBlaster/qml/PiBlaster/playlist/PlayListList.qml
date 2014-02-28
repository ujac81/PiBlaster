import QtQuick 2.0

ListView {

    anchors.fill: parent
    clip: true

    model: PlayListModel{}
    delegate: Rectangle {
        id: browseDelegate
        width: parent.width
        height: root.baseFontSize * 1.8
        clip: true

        color: active ? root.colorSelected : (index % 2 == 0 ? root.colorUnselected : root.colorUnselected2 )


        Text {
            id: plitem
            anchors.fill: parent
            text: title
        }



        MouseArea {
            id: pl_elements_click_check
            anchors.fill: parent
            onClicked: {

            }
            onDoubleClicked: {

            }
            onPressAndHold: {

            }
        }
    }
}
