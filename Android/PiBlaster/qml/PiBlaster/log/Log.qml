import QtQuick 2.0

/**
 * Display status messages for RFCOMM communication
 *
 * Messages received via cpp -> java interface
 */
Rectangle {
    id: log
    anchors.fill: parent
    color: "black"

    Text {
        id: logText
        anchors.fill: parent
        text: "Log opened.\n"
        wrapMode: Text.WrapAnywhere
        color: "white"
        font.pixelSize: 20
    }

    function activated()
    {
        logText.text = "Log opened....\n";
        var count = rfcommClient.initAndCountBluetoothMessages
        for(var i = 0; i < count; i++)
        {
            logText.text += "--> " + rfcommClient.nextBluetoothMessage + "\n";
        }
    }
}
