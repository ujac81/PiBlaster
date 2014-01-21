

import QtQuick 2.0

//import "../browse"
//import "../connect"
//import "../log"
//import "../playlist"
//import "../search"
//import "../settings"

// Includes the UI with tab bars and the item model for the central objects
Rectangle {

    color: "transparent"

    property alias tabbedUI: tabUI
    property alias tabsModel: tabsModel
    focus: true


    // holds all central objects -- enabled and disabled by TabbedUI
    VisualItemModel {

        id: tabsModel

        Item {
            property alias loader: pageloader0
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader0 }
            function load() {
                pageloader0.source = "../playlist/Playlist.qml"
            }
        }
        Item {
            property alias loader: pageloader1
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader1; focus: true }
            function load() {
                pageloader1.source = "../browse/Browse.qml"
            }
        }
        Item {
            property alias loader: pageloader2
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader2 }
            function load() {
                pageloader2.source = "../search/Search.qml"
            }
        }
        Item {
            property alias loader: pageloader3
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader3 }
            function load() {
                pageloader3.source = "../connect/Connect.qml"
            }
        }
        Item {
            property alias loader: pageloader4
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader4 }
            function load() {
                pageloader4.source = "../log/Log.qml"
            }
        }
        Item {
            property alias loader: pageloader5
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader5 }
            function load() {
                pageloader5.source = "../settings/Settings.qml"
            }
        }
    }

    // main user interface
    TabbedUI {
        id: tabUI
        tabsModel: tabsModel
        anchors.fill: parent
    }

}
