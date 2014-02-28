import QtQuick 2.0


ListModel {
    id: playlistModel

    function clearAll() {
        clear();
    }

    /**
     * Send showplaylist request to PyBlaster
     * Answer will be received by RFCommRecvThread and will be received
     * as QT signal.
     *
     */
    function reload_playlist() {

        clearAll();

        rfcomm.execCommand("plshow 0 0 100 0");

    }

    /**
     * Called by main if shwowdevices message received from PI
     */
    function received_playlist(msg) {
        clearAll();

        if ( msg.status() == 0 ) {
            for ( var i = 0; i < msg.payloadSize(); i++ ) {
                var arr = msg.payloadElements(i);
                append({"position": arr[0],
                        "state": arr[1],
                        "title": arr[2],
                        "active": ( arr[1] == "2" )
                       });
            }
        } else {
            root.log_error("Bad return status for 'plshow'");
        }
    }
}

