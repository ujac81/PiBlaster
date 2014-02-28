import QtQuick 2.0

Rectangle {

    id: playlist
    anchors.fill: parent
    color: "transparent"


    Column
    {
        anchors.fill: parent
        spacing: 20


        Text {
            id: playTitleText

            text: "Title"
        }
        Text {
            id: playArtistText

            text: "Artist"
        }
        Text {
            id: playAlbumText

            text: "Album"
        }
        Text {
            id: playYearText

            text: "Year"
        }
        Text {
            id: playGenreText

            text: "Genre"
        }

        Rectangle
        {
            height: 56
            width: parent.width
            color: "transparent"

            Row {
                anchors.centerIn: parent
                height: 48
                spacing: 30

                Image {
                    source: "qrc:///images/images/prev.png"
                    width: parent.height
                    height: parent.height
                    MouseArea {
                        anchors.fill: parent
                        onClicked: prev()
                    }
                }
                Image {
                    id: playPlayImage
                    source: "qrc:///images/images/play.png"
                    width: parent.height
                    height: parent.height
                    MouseArea {
                        anchors.fill: parent
                        onClicked: playpause()
                    }

                    function showPlay(play) {
                        if (play) {
                            source = "qrc:///images/images/play.png";
                        } else {
                            source = "qrc:///images/images/pause.png";
                        }
                    }
                }
                Image {
                    source: "qrc:///images/images/next.png"
                    width: parent.height
                    height: parent.height
                    MouseArea {
                        anchors.fill: parent
                        onClicked: next()
                    }
                }
            }
        }

    }

    //////////////////////////// TRIGGERS ////////////////////////////

    /**
     * Called upon tab select.
     * Check if connected, if not raise connect overlay.
     */
    function activated() {
        if (root.connected()) refresh();
    }

    /**
     * Triggered via main if this view is active and we got back key.
     */
    function handleBackKey() {
        return false;
    }

    /**
     * Triggered by main if playstatus received
     */
    function gotPlayStatus(msg) {
        if ( msg.status() != 0 ) {
            playTitleText.text = "No Playlist";
            playAlbumText.text = "";
            playArtistText.text = "";
            playYearText.text = "";
            playGenreText.text = "";
            playPlayImage.showPlay(1);
        } else {
            var arr = msg.payloadElements(0);
            playTitleText.text = arr[6];
            playAlbumText.text = arr[7];
            playArtistText.text = arr[8];
            playYearText.text = arr[10];
            playGenreText.text = arr[9];

            if (arr[0] == "0")
                playPlayImage.showPlay(1);
            else
                playPlayImage.showPlay(arr[2]=="1");
        }
    }

    function refresh() {
        rfcomm.execCommand("playstatus");
    }

    function prev() {
        rfcomm.execCommand("playprev");
    }

    function playpause() {
        rfcomm.execCommand("playpause");
    }

    function next() {
        rfcomm.execCommand("playnext");
    }


}
