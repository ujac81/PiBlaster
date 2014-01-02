import QtQuick 2.0

Rectangle {

    id: tabbedUI
    color: "transparent"
    anchors.fill: parent

    property int tabsHeight : 30
    property int tabIndex : 3

    // central objects from Tabview
    property VisualItemModel tabsModel


    // create all tab views embedded into tab bar
    Rectangle {
        id: tabViewContainer
        width: parent.width
        color: "transparent"

        anchors.top: tabBarTop.bottom
        anchors.bottom: tabBarBottom.top

        Repeater {
            model: tabsModel
        }
    }

    // hide all the tab views and select default tab
    Component.onCompleted:
    {
        for(var i = 0; i < tabsModel.children.length; i++)
        {
            tabsModel.children[i].visible = false;
        }
        tabClicked(tabIndex);
    }

    // hide old tab and show new tab
    function tabClicked(index)
    {
        if (tabIndex < 3)
            topTabs.children[tabIndex].color = "transparent";
        else
            bottomTabs.children[tabIndex-3].color = "transparent";

        tabsModel.children[tabIndex].visible = false;
        tabIndex = index;


        if (tabIndex < 3)
            topTabs.children[tabIndex].color = "#0A89FF";
        else
            bottomTabs.children[tabIndex-3].color = "#0A89FF";

        tabsModel.children[tabIndex].visible = true;
    }


    // top tab bar
    Rectangle {
        id: tabBarTop
        height: tabbedUI.tabsHeight
        color: "transparent"

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

        // place all the tabs in a row
        Row {
            anchors.fill: parent
            width: parent.width
            id: topTabs

            Button { width: parent.width / 3; height: parent.height; index: 0; text: "Playlist" }
            Button { width: parent.width / 3; height: parent.height; index: 1; text: "Browse" }
            Button { width: parent.width / 3; height: parent.height; index: 2; text: "Manage" }
        }
    }

    // top tab bar
    Rectangle {
        id: tabBarBottom
        height: tabbedUI.tabsHeight
        color: "transparent"

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        // place all the tabs in a row
        Row {
            anchors.fill: parent
            width: parent.width
            id: bottomTabs

            Button { width: parent.width / 3; height: parent.height; index: 3; text: "Connect" }
            Button { width: parent.width / 3; height: parent.height; index: 4; text: "Log" }
            Button { width: parent.width / 3; height: parent.height; index: 5; text: "Settings" }
        }
    }



}
