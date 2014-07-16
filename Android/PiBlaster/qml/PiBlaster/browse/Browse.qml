import QtQuick.Controls 1.2
import QtQuick 2.0

import "../items"


/**
 * Browse view -- holds ListView of browseable items
 *
 */
Rectangle {

    id: browse
    anchors.fill: parent
    color: "transparent"
    focus: true

    property alias pathText: pathText.text


    //////////////////////////// OVERLAYS ////////////////////////////

    // Question dialog if dirs should be added.
    // Invoked if dirs in selection found.
    // Invokes model.addToPlaylist(mode)
    // Set addMode bevore raise with show()
    MessageWindow {
        id: addDirsDialog
        property int addMode: -1 // remember mode while waiting for dialog to close
        boxHeight: 400

        caption: "Add directories"
        text: "Directories will be added recursively. Your selection contains directories. Adding directories to playlists is allowed, but may result in huge playlists."

        onAccepted: browse.addToPlaylist(addMode)
    }

    // Add elements dialog
    Item {
        id: addDialog
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
                        onPressed: addDialog.close()
                    }
                }
            }

            Column {

                anchors.centerIn: parent
                anchors.top: header.bottom

                width: parent.width - 2 * root.buttonSpacing
                spacing: root.buttonSpacing

                Button {
                    id: browseAppend
                    text: "Append"
                    width: parent.width
                    onPressed: addDialog.append(0);
                }
                Button {
                    id: browseInsertAfterCurrent
                    text: "Insert after current"
                    width: parent.width
                    onPressed: addDialog.append(1);
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
            if ( browseList.model.checkDirsInSelection() == 1 ) {
                addDirsDialog.addMode = mode;
                addDirsDialog.show();
            }
            else
                browse.addToPlaylist(mode)
            close();
        }

        function show() {
            if ( browseList.model.checkAnyThingSelected() )
                opacity = 1;
        }
    } // end Item for add overlay


    /**
     * Connect button overlay -- raised if not connected.
     * Show connect button if root.connected() is false and switch to connect tab.
     */
    Item {
        id: connectOverlay
        z: 101
        anchors.fill: parent
        visible: opacity !== 0
        opacity: 0

        // Fill complete area with MouseArea to catch touch events
        Rectangle {
            anchors.fill: parent
            color: "#000000"
            opacity: 0.6
            MouseArea { anchors.fill: parent }
        }

        // animate opacity, 250ms to raise/fall
        Behavior on opacity {
            NumberAnimation { duration: 250 }
        }

        Button {
            id: browseConnectButton
            anchors.centerIn: parent
            text: "Connect"
            onPressed: root.tabview.tabbedUI.tabClicked(3);
        }

        function show() {
            if (! root.connected())
                opacity = 1;
            else
            {
                opacity = 0;
                browseList.model.request_load("root", "root");
            }
        }
    }


    //////////////////////////// CENTRAL WINDOW ////////////////////////////


    ////////////// top tool bar //////////////

    Rectangle {
        id: browseToolBar
        height: 56
        anchors.top: parent.top
        width: parent.width
        color: "#66666666"

        Row {
            id: browseButtonRow
            height: 48
            anchors.centerIn: parent
            spacing: 4

            Image {
                id: browseHomeButton
                source: "qrc:///images/images/home.png"
                width: parent.height
                height: parent.height
                MouseArea {
                    anchors.fill: parent
                    onClicked: browseList.model.request_load("root", "root")
                }
            }
            Image {
                id: browseUpButton
                source: "qrc:///images/images/up.png"
                width: parent.height
                height: parent.height
                MouseArea {
                    anchors.fill: parent
                    onClicked: browseList.model.dir_up()
                }
            }

            LineInput {
                id: browseQuickFilter
                height: parent.height - 8
                y: 4
                width: browseToolBar.width - 3*parent.height - 3*4

                onEnterPressed: console.log("Filter: "+ browseQuickFilter.text)
                onCleared: console.log("Filter cleared")


            }
            Image {
                id: browseAddButton
                source: "qrc:///images/images/add.png"
                width: parent.height
                height: parent.height

                MouseArea {
                    anchors.fill: parent
                    onClicked: addDialog.show()
                }
            }
        }
    }

    ////////////// path field //////////////

    Rectangle {
        id: pathBox
        anchors.top: browseToolBar.bottom
        width: parent.width
        color: "#22222222"
        height: 2 * root.baseFontSize

        Text {
            id: pathText
            text: "PATH HERE"
            font.pixelSize: root.baseFontSize
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideLeft

            function changePath(path) {
                text = path;
            }

            Component.onCompleted: browseList.model.onPathChanged.connect(changePath);
        }
    }


    ////////////// central list view //////////////

    Rectangle {
        id: browseBox
        anchors.top: pathBox.bottom
        anchors.bottom: parent.bottom
        width: parent.width
        color: "transparent"

        ScrollView {
            anchors.fill: parent
            BrowseList{ id: browseList }
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
        connectOverlay.show();
    }

    /**
     * Triggered via main if this view is active and we got back key.
     * If not on top dir, go up one dir, otherwise do not handle back event.
     */
    function handleBackKey() {
        if ( browseList.model.on_root_dir() )
            return false;
        browseList.model.dir_up();
        return true;
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

        browseList.model.push_to_playlist_send_list(add_mode)
        // waitOverlay will now block view until signal from rfcomm received
    }

    /// called by main on receive of showdevice data
    function received_showdev_data(msg) {
        browseList.model.received_devices(msg);
    }

    /// called by main on receive of lsfulldir data
    function received_dir_data(msg) {
        browseList.model.received_dir(msg);
    }

}
