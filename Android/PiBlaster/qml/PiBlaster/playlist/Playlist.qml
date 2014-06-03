import QtQuick 2.0

import "../items"

Rectangle {

    id: playlist
    anchors.fill: parent
    color: "transparent"


    ////////////////// TOP MENU BAR //////////////////

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


    ////////////////// BOTTOM MENU BAR //////////////////

    Rectangle {
        id: plMenuBarBot
        height: root.barHeight + 5
        color: "transparent"

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        Row {
            anchors.top: parent.top
            width: parent.width
            height: root.barHeight
            id: plMenuTabsBot

            Tab { width: parent.width / 3; height: parent.height; index: 3; text: "Remove" }
            Tab { width: parent.width / 3; height: parent.height; index: 4; text: "Play next" }
            Tab { width: parent.width / 3; height: parent.height; index: 5; text: "To end" }
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
        anchors.bottom: plMenuBarBot.top
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
     * Triggered via main if this view is active and we got back key.
     */
    function handleBackKey() {
        return false;
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
        if ( index == 3 ) {
            playlistlist.model.modify_playlist(1)
        }
        if ( index == 4 ) {
            playlistlist.model.modify_playlist(2)
        }
        if ( index == 5 ) {
            playlistlist.model.modify_playlist(3)
        }


    }

    function received_pl_data(msg) {
        playlistlist.model.received_playlist(msg);
    }
}
