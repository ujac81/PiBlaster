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

            text: "Title"
        }
        Text {

            text: "Artist"
        }
        Text {

            text: "Album"
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
                }
                Image {
                    source: "qrc:///images/images/next.png"
                    width: parent.height
                    height: parent.height
                    MouseArea {
                        anchors.fill: parent
                        onClicked: next
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

    }

    /**
     * Triggered via main if this view is active and we got back key.
     */
    function handleBackKey() {
        return false;
    }


    function prev() {

    }

    function playpause() {

    }

    function next() {

    }


}
