import QtQuick.Controls 1.2
import QtQuick 2.0

import "../items"


/**
 * Search tab in main tab view
 *
 */
Rectangle {

    id: search
    anchors.fill: parent
    color: "transparent"
    focus: true

    //////////////////////////// OVERLAYS ////////////////////////////

    // Add elements dialog
    Item {
        id: searchAddDialog
        z: 50
        anchors.fill: parent
        visible: opacity !== 0
        // show() will raise opacity
        opacity: 0

        // Fill complete area with MouseArea to catch touch events
        Rectangle {
            anchors.fill: parent
            color: "#000000"
            opacity: 0.6
            MouseArea { anchors.fill: parent }
        }

        ButtonBox {

            anchors.centerIn: parent
            width: 300
            height: 300

            Rectangle {
                id: header
                width: parent.width
                anchors.top: parent.top

                height: root.buttonHeight
                radius: 10
                border.width: 4
                border.color:  root.colorButtonBoxFrame
                color: "white"

                Text {
                    anchors.centerIn: parent
                    anchors.rightMargin: root.buttonHeight + 5
                    color: root.buttonColorActiveText
                    font.pixelSize: root.baseFontSize
                    text: "Add to Playlist      "
                }

                Rectangle {
                    height: root.buttonHeight
                    width: root.buttonHeight * 1.5
                    anchors.right: parent.right
                    anchors.top: parent.top

                    radius: 10
                    border.width: 4
                    border.color:  root.colorButtonBoxFrame
                    color: root.buttonColorInactive

                    Image {
                        anchors.centerIn: parent
                        width: root.buttonHeight - 15
                        height: root.buttonHeight - 15
                        source: "qrc:///images/images/x-nopad.png"
                    }
                    MouseArea {
                        anchors.fill: parent
                        onPressed: searchAddDialog.close()
                    }
                }
            }

            Column {

                anchors.centerIn: parent
                anchors.top: header.bottom

                width: parent.width - 2 * root.buttonSpacing
                spacing: root.buttonSpacing

                Button {
                    id: searchAppend
                    text: "Append"
                    width: parent.width
                    onPressed: searchAddDialog.append(0);
                }
                Button {
                    id: searchInsertAfterCurrent
                    text: "Insert after current"
                    width: parent.width
                    onPressed: searchAddDialog.append(1);
                }
            }
        }

        // animate opacity, 250ms to raise/fall
        Behavior on opacity {
            NumberAnimation { duration: 250 }
        }

        function close() {
            opacity = 0;
        }

        function append(mode) {
            search.addToPlaylist(mode)
            close();
        }

        function show() {
            if ( searchList.model.checkAnyThingSelected() )
                opacity = 1;
        }
    } // end Item for add overlay


    //////////////////////////// CENTRAL WINDOW ////////////////////////////


    ////////////// top tool bar //////////////

    Rectangle {
        id: searchToolBar
        height: 56
        anchors.top: parent.top
        width: parent.width
        color: "#66666666"

        Row {
            id: searchButtonRow
            height: 48
            anchors.centerIn: parent
            spacing: 4

            Image {
                id: searchSearchButton
                source: "qrc:///images/images/search.png"
                width: parent.height
                height: parent.height
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        console.log("Search: "+ searchSearchBar.text);
                        searchList.model.request_search(searchSearchBar.text);
                    }
                }
            }

            LineInput {
                id: searchSearchBar
                height: parent.height - 8
                text: "search"
                y: 4
                width: searchToolBar.width - 2*parent.height - 3*4

                onEnterPressed: {
                    console.log("Search: "+ searchSearchBar.text);
                    searchList.model.request_search(searchSearchBar.text);
                }
                onCleared: console.log("Search cleared")
            }
            Image {
                id: searchAddButton
                source: "qrc:///images/images/add.png"
                width: parent.height
                height: parent.height

                MouseArea {
                    anchors.fill: parent
                    onClicked: searchAddDialog.show()
                }
            }
        }
    }

    ////////////// central list view //////////////

    Rectangle {
        id: searchBox
        anchors.top: searchToolBar.bottom
        anchors.bottom: parent.bottom
        width: parent.width
        color: "transparent"

        ScrollView {
            anchors.fill: parent
            SearchList{ id: searchList }
        }
    }


    /**
     */
    Component.onCompleted: {
    }

    //////////////////////////// TRIGGERS ////////////////////////////

    /**
     * Called upon tab select.
     * Check if connected, if not raise connect overlay.
     */
    function activated() {
    }

    /**
     * Triggered via main if this view is active and we got back key.
     * Do not handle back event.
     */
    function handleBackKey() {
        return false;
    }


    //////////////////////////// HELPERS ////////////////////////////

    /**
     * Raise wait overlay and invoke RFCOMMClient::sendPlaylistAdd().
     * This will fire up a send thread which will send a signal
     * addToPlaylistFinished(msg) which is connected to addFinished here.
     */
    function addToPlaylist(add_mode) {
        waitOverlay.caption = "Adding to playlist";
        waitOverlay.text = "Please stand by while adding to playlist...";
        waitOverlay.show();

        searchList.model.push_to_playlist_send_list(add_mode)
        // waitOverlay will now block view until signal from rfcomm received
    }


    /// called by main on receive of search data
    function received_search_data(msg) {
        searchList.model.received_search(msg);
    }


}
