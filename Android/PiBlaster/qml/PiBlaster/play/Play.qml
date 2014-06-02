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
            } // buttons row
        } // buttons rect

        // Volume slider width vol=0 and vol=100 endcaps
        Row {
            width: parent.width
            height: 48
            spacing: 0

            Rectangle {
                height: parent.height
                width: 40
                color: "transparent"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rfcomm.execCommand("volset 0");
                    }
                }
            }

            Rectangle {
                id: playVolumeBar
                // anchors.fill: parent
                width: parent.width - 80
                height: parent.height
                color: "transparent"
                radius: 10
                border.width: 4
                border.color:  root.colorButtonBoxFrame

                Text {
                    id: playVolumeText
                    anchors.centerIn: parent
                    text: "volume"
                    color: "black"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        var vol = Math.round((mouseX-x)/width*100.);
                        rfcomm.execCommand("volset "+vol);
                    }
                }

                Rectangle {
                    id: playVolumeSliderPos
                    height: parent.height
                    x: 0
                    width: parent.width / 2
                    clip: true
                    color: "#39393908"
                    z: parent.z - 1
                    radius: 10
                }

                function showVol(vol) {
                    var nw = Math.round(vol/100. * width);
                    playVolumeText.text = vol
                    playVolumeSliderPos.width = Math.min(width, nw);
                }
            } // volumeBar rect

            Rectangle {
                color: "transparent"
                height: parent.height
                width: 40
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rfcomm.execCommand("volset 100");
                    }
                }
            }
        } // vol row
    } // play col

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

            playVolumeBar.showVol(arr[12]);
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
