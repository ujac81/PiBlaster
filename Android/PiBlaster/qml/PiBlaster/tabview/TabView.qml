

import QtQuick 2.0

import "../browse"
import "../log"
import "../play"
import "../playlist"
import "../search"
import "../settings"

// Includes the UI with tab bars and the item model for the central objects
Rectangle {

    color: "transparent"

    property alias tabbedUI: tabUI
    property alias tabsModel: tabsModel
    focus: true


    // holds all central objects -- enabled and disabled by TabbedUI
    VisualItemModel {

        id: tabsModel

        Play {}
        Playlist {}
        Browse {}
        Search {}
        Log {}
        Settings {}

    }

    // main user interface
    TabbedUI {
        id: tabUI
        tabsModel: tabsModel
        anchors.fill: parent
    }


    function browseTab() { return tabsModel.children[2]; }
    function playlistTab() { return tabsModel.children[1]; }

    function currentTab() { return tabsModel.children[tabUI.tabIndex]; }

}
