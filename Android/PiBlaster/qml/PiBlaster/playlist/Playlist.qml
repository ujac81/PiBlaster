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

    //////////////////////////// OVERLAYS ////////////////////////////

    // Question dialog if playlist should be cleared
    // Invoked clear pressed
    // Invokes playlistlist.model.clear_playlist()
    MessageWindow {
        id: clearPlaylistDialog
        boxHeight: 300

        caption: "Clear Playlist"
        text: "Playlist will be cleared out. It's not possible to restore cleared playlists!"

        onAccepted: playlistlist.model.clear_playlist()
    }



    ////////////////// CENTRAL LIST VIEW //////////////////

    Rectangle {
        anchors.top: plMenuBar.bottom
        anchors.bottom: parent.bottom
        width: parent.width

        PlayListList {
            id: playlistlist
            anchors.fill: parent
        }

    }

    ////////////////// FUNCTIONS //////////////////

    /**
     * Called when tab activated in tab view
     */
    function activated() {
        playlistlist.model.reload_playlist();
    }

    /**
     * Next song started -- hilight next item
     */
    function gotPlayStatus(msg) {
        playlistlist.model.gotPlayStatus(msg);
    }

    function tabClicked(index) {

        if ( index == 2 ) {
            clearPlaylistDialog.show();
        }
    }

    function received_pl_data(msg) {
        playlistlist.model.received_playlist(msg);
    }
}
