import QtQuick 2.0

import "../items"

Rectangle {

    id: playlist
    anchors.fill: parent
    color: "transparent"


    ////////////////// MENU BAR //////////////////

    Rectangle {
        id: plMenuBar
        height: root.barHeight + 5
        color: "transparent"

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

        Row {
            anchors.bottom: parent.bottom
            width: parent.width
            height: root.barHeight
            id: plMenuTabs

            Tab { width: parent.width / 3; height: parent.height; index: 0; text: "Save as" }
            Tab { width: parent.width / 3; height: parent.height; index: 1; text: "Load" }
            Tab { width: parent.width / 3; height: parent.height; index: 2; text: "Clear" }
        }


    }



    ////////////////// CENTRAL LIST VIEW //////////////////


    PlayListList {
        id: playlistlist
        anchors.top: plMenuBar.bottom
        anchors.bottom: parent.bottom
        width: parent.width
    }



    ////////////////// FUNCTIONS //////////////////

    /**
     * Called when tab activated in tab view
     */
    function activated() {
        playlistlist.model.reload_playlist();
    }

    function tabClicked(index) {
        console.log("PL tab selected "+index)
    }

    function received_pl_data(msg) {
        playlistlist.model.received_playlist(msg);
    }
}
