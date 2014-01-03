import QtQuick 2.0

import "../items"

Rectangle {

    id: tabbedUI
    color: "transparent"
    anchors.fill: parent

    property int tabIndex : 3 // connect button should be selected on start

    property VisualItemModel tabsModel


    // create all tab views placed between both tab bars
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

    /**
     * Hide old tab and show new tab clicked
     * Invoke activated() function of selected tab
     */
    function tabClicked(index)
    {
        if (tabIndex < 3)
            topTabs.children[tabIndex].color = root.buttonColorActive
        else
            bottomTabs.children[tabIndex-3].color = root.buttonColorActive

        tabsModel.children[tabIndex].visible = false;
        tabIndex = index;


        if (tabIndex < 3)
            topTabs.children[tabIndex].color = root.buttonColorPressed;
        else
            bottomTabs.children[tabIndex-3].color = root.buttonColorPressed;


        tabsModel.children[tabIndex].visible = true;
        tabsModel.children[tabIndex].activated()
    }


    // top tab bar
    Rectangle {
        id: tabBarTop
        height: root.barHeight
        color: "transparent"

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

        Row {
            anchors.fill: parent
            width: parent.width
            id: topTabs

            Tab { width: parent.width / 3; height: parent.height; index: 0; text: "Playlist" }
            Tab { width: parent.width / 3; height: parent.height; index: 1; text: "Browse" }
            Tab { width: parent.width / 3; height: parent.height; index: 2; text: "Search" }
        }
    }

    // bottom tab bar
    Rectangle {
        id: tabBarBottom
        height: root.barHeight
        color: "transparent"

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        Row {
            anchors.fill: parent
            width: parent.width
            id: bottomTabs

            Tab { width: parent.width / 3; height: parent.height; index: 3; text: "Connect" }
            Tab { width: parent.width / 3; height: parent.height; index: 4; text: "Log" }
            Tab { width: parent.width / 3; height: parent.height; index: 5; text: "Settings" }
        }
    }



}
