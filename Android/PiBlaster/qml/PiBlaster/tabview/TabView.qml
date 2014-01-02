import QtQuick 2.0



// Includes the UI with tab bars and the item model for the central objects
Rectangle {

    color: "transparent"

    // holds all central objects -- enabled and disabled by TabbedUI
    VisualItemModel {

        id: tabsModel

        Tabplaylist { id: tabPlaylist }
        Tabbrowse { id: tabBrowse }
        Tabmanage { id: tabManage }
        Tabconnect { id: tabConnect }
        Tablog { id: tabLog }
        Tabsettings { id: tabSettings }


    }

    // main user interface
    TabbedUI {
        id: tabUI
        tabsModel: tabsModel
        anchors.fill: parent
    }



}
