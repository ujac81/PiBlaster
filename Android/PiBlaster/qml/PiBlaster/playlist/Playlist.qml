import QtQuick 2.0

import "../items"

Rectangle {

    id: playlist
    anchors.fill: parent
    color: "transparent"


    ////////////////// MENU Button //////////////////

    Rectangle {
        id: plMenuBar
        height: root.barHeight + 5
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        width: parent.width
        color: "transparent"

        Tab {
            anchors.bottom: parent.bottom
            width: parent.width
            height: root.barHeight
            id: plMenuTab
            text: "Menu"
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

    // Menu overlay
    Item {
        z: 99
        id: plMenu
        visible: opacity != 0
        opacity: 0

        Rectangle {
            anchors.top: plMenuBar.bottom
            anchors.left: plMenuBar.left
            width: 300
            height: 350
            color: root.colorButtonBox

            MouseArea { anchors.fill: parent }

            Column {
                anchors.centerIn: parent
                width: parent.width
                spacing: 5

                Tab { width: parent.width; height: root.barHeight; index: 0; text: "Menu" }
                Tab { width: parent.width; height: root.barHeight; index: 1; text: "Save as" }
                Tab { width: parent.width; height: root.barHeight; index: 2; text: "Load" }
                Tab { width: parent.width; height: root.barHeight; index: 3; text: "Delete" }
                Tab { width: parent.width; height: root.barHeight; index: 4; text: "Clear selection" }
                Tab { width: parent.width; height: root.barHeight; index: 5; text: "Selection after current" }
                Tab { width: parent.width; height: root.barHeight; index: 6; text: "Selection to end" }
                Tab { width: parent.width; height: root.barHeight; index: 7; text: "Randomize all" }
            }
        }
        function toggleShow() {
            plMenu.opacity = ! plMenu.opacity
        }
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
        plMenu.toggleShow();
        if ( index == 3 ) clearPlaylistDialog.show();
        if ( index == 4 ) playlistlist.model.modify_playlist(1);
        if ( index == 5 ) playlistlist.model.modify_playlist(2);
        if ( index == 6 ) playlistlist.model.modify_playlist(3);
    }

    function received_pl_data(msg) {
        playlistlist.model.received_playlist(msg);
    }
}
