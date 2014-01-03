

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


    // holds all central objects -- enabled and disabled by TabbedUI
    VisualItemModel {

        id: tabsModel

        Item {
            property alias loader: pageloader0
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader0 }
            function load() {
                pageloader0.source = "../playlist/Playlist.qml"
//                pageloader0.item.activated()
            }
        }
        Item {
            property alias loader: pageloader1
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader1 }
            function load() {
                pageloader1.source = "../browse/Browse.qml"
//                pageloader1.item.activated()
            }
        }
        Item {
            property alias loader: pageloader2
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader2 }
            function load() {
                pageloader2.source = "../search/Search.qml"
//                pageloader2.item.activated()
            }
        }
        Item {
            property alias loader: pageloader3
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader3 }
            function load() {
                pageloader3.source = "../connect/Connect.qml"
//                pageloader3.item.activated()
            }
        }
        Item {
            property alias loader: pageloader4
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader4 }
            function load() {
                pageloader4.source = "../log/Log.qml"
//                pageloader4.item.activated()
            }
        }
        Item {
            property alias loader: pageloader5
            anchors.fill: parent
            Loader { anchors.fill: parent; id: pageloader5 }
            function load() {
                pageloader5.source = "../settings/Settings.qml"
//                pageloader5.item.activated()
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
