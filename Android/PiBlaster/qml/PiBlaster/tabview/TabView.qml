

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


    // holds all central objects -- enabled and disabled by TabbedUI
    VisualItemModel {

        id: tabsModel

        Playlist { id: playlist }
        Browse { id: browse }
        Search { id: search }
        Connect { id: connect }
        Log { id: log }
        Settings { id: settings }
    }

    // main user interface
    TabbedUI {
        id: tabUI
        tabsModel: tabsModel
        anchors.fill: parent
    }

}
