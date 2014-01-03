import QtQuick 2.0

import "../items"


/**
 * Browse view -- holds ListView of browseable items
 *
 */
Rectangle {
    anchors.fill: parent
    color: "transparent"

    Rectangle {
        id: browseBox
        anchors.fill: parent
        color: "transparent"

        ListView {
            id: browseList
            anchors.fill: parent
            clip: true

            model: BrowseModel{}
            delegate: Rectangle {
                id: browseDelegate
                width: parent.width
                height: root.baseFontSize * 3.8
                clip: true

                color: selected ? root.colorSelected : (index % 2 == 0 ? root.colorUnselected : root.colorUnselected2 )

                Row {
                    width: parent.width
                    // usb devices and folders get extra image column
                    // media files (type == 2) do not get prefix
                    Text {
                        id: rowimg
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        text: type == 0 ? '<img src="qrc:///images/images/usb.png" width="32px" height="32px"/>' :
                                ( type == 1 ? '<img src="qrc:///images/images/folder.png" width="32px" height="32px"/>'  :
                                  "" )
                        width: type < 2 ? 40 : 0
                        verticalAlignment: Text.AlignBottom
                    }
                    // entry, content created via BrowseModel.itemText()
                    Text {
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.right: parent.right
                        anchors.left: rowimg.right
                        textFormat: Text.RichText
                        text: browseList.model.itemText(index)
                        font.pixelSize: root.baseFontSize
                    }
                }

                MouseArea {
                    id: elements_click_check
                    anchors.fill: parent
                    onClicked: {
                        if ( browseList.model.get(index).type != 0 ) {
                            browseList.model.get(index).selected = ! browseList.model.get(index).selected
                        }
                    }
                    onDoubleClicked: {
                        if ( browseList.model.get(index).type == 0 ) {
                            browseList.model.load(browseList.model.get(index).storid+" 0");
                        } else if ( browseList.model.get(index).type == 1 ) {
                            browseList.model.load(browseList.model.get(index).storid+" "+
                                                  browseList.model.get(index).dirid);
                        }
                    }
                }
            }
        }
    }


    Button {
        id: browseConnectButton
        anchors.centerIn: parent
        text: "Connect"

        MouseArea {
            anchors.fill: parent
            onClicked: {
                root.tabview.tabbedUI.tabClicked(3);
            }
            onPressed: { if ( parent.active ) { parent.color = root.buttonColorPressed; } }
            onReleased: { if ( parent.active ) { parent.color = root.buttonColorActive; } }
        }
    }

    states: [
        State {
            name: "StateNotConnected"
            PropertyChanges { target: browseBox; visible: false }
            PropertyChanges { target: browseConnectButton; visible: true }
        },
        State {
            name: "StateConnected"
            PropertyChanges { target: browseBox; visible: true }
            PropertyChanges { target: browseConnectButton; visible: false }
        }
    ]

    function activated() {
        if (! connect.connected) {
            state = "StateNotConnected";
        } else {
            state = "StateConnected";
            browseList.model.load("root");
        }
    }
}
