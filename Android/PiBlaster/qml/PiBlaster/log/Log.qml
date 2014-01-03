import QtQuick 2.0

/**
 * Display status messages for RFCOMM communication
 *
 * Messages received via cpp -> java interface
 */
Rectangle {
    anchors.fill: parent
    color: "black"

    Text {
        id: log
        anchors.fill: parent
        text: "Log opened.\n"
        wrapMode: Text.WrapAnywhere
        color: "white"
        font.pixelSize: 20
    }

    function activated()
    {
        log.text = "Log opened....\n";
        var count = rfcommClient.initAndCountBluetoothMessages
        for(var i = 0; i < count; i++)
        {
            log.text += "--> " + rfcommClient.nextBluetoothMessage + "\n";
        }
    }
}
