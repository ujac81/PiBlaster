

import QtQuick 2.0

import "../browse"
import "../connect"
import "../log"
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

        Playlist {}
        Browse {}
        Search {}
        Connect {}
        Log {}
        Settings {}

    }

    // main user interface
    TabbedUI {
        id: tabUI
        tabsModel: tabsModel
        anchors.fill: parent
    }

}
