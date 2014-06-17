import QtQuick 2.0


ListModel {
    id: searchModel

    function clearAll() {
        clear();
    }

    /**
     * Send browse request to PyBlaster
     * Answer will be received by RFCommRecvThread and will be received
     * as QT signal.
     */
    function request_search(pattern) {

        clearAll(); // delete already upon request to prevent mutiple request while user should wait.

        rfcomm.execCommand("search 1 200 "+pattern);
    }

    /**
     * Called by main if shwowdevices message received from PI
     */
    function received_search(msg) {
        clearAll();

        if ( msg.status() == 0 ) {
            for ( var i = 0; i < msg.payloadSize(); i++ ) {
                var arr = msg.payloadElements(i);
                // [[usbid, dirid, fileid, time, artist, album, title, path]]
                append({"storid": arr[0],
                        "dirid": arr[1],
                        "fileid": arr[2],
                        "time": arr[3],
                        "artist": arr[4],
                        "album": arr[5],
                        "title": arr[6],
                        "path": arr[7],
                        "selected": false,
                       });
            }
        } else {
            root.log_error("Bad return status for 'showdevices'");
        }
    }


    /**
     * True if any item selected
     */
    function checkAnyThingSelected() {
        for ( var i = 0; i < count; i++ ) {
            if ( get(i).selected ) return true;
        }
        return false;
    }

    /**
     * Invoke playlist append function
     * Args:
     *  - 1: append to playlist
     *  - 2: append after current
     *  - 3: random insert
     */
    function push_to_playlist_send_list(add_mode)
    {
        console.log("addToPlaylist("+add_mode+") called.");

        rfcomm.clearSendPayload();

        for ( var i = 0; i < count; i++ )
        {
            var elem = get(i);
            if ( elem.selected )
            {
                rfcomm.addToSendPayload("FILE "+elem.storid+" "+elem.dirid+" "+elem.fileid);
            }
        }
        deselect_all();
        rfcomm.execCommandWithPayload("plappendmultiple "+add_mode);
    }

    /**
     * Set all selected properties to false in current view.
     * Called after addToPlaylist()
     */
    function deselect_all() {
        for ( var i = 0; i < count; i++ ) {
            get(i).selected = false;
        }
    }
}

