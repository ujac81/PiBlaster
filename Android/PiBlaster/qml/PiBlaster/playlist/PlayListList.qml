import QtQuick 2.0

ListView {

    clip: true
    model: PlayListModel{}

    delegate: Rectangle {
        id: browseDelegate
        width: parent.width
        height: root.baseFontSize * 1.8
        clip: true

        color: active ? root.colorSelected2 :
                        ( selected ? root.colorSelected :
                                     ( index % 2 == 0 ? root.colorUnselected :
                                                        root.colorUnselected2 )
                         )

        Text {
            id: plitem
            anchors.fill: parent
            text: title
        }

        MouseArea {
            id: pl_elements_click_check
            anchors.fill: parent
            onClicked: {
                if ( playlistlist.model.get(index).type != 0 ) {
                    playlistlist.model.get(index).selected = ! playlistlist.model.get(index).selected
                }
            }
            onDoubleClicked: {
                var elem = playlistlist.model.get(index);
                playlistlist.model.set_all_inactive();
                elem.active = true;
                playlistlist.model.jump_to_tune(elem.position);
            }
            onPressAndHold: {

            }
        }
    }
}

