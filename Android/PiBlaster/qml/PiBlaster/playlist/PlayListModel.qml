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

        rfcomm.execCommand("plshow 0 0 500 0");
    }



    /**
     * Let PyBlaster clear its current active playlist
     */
    function clear_playlist() {
        clearAll();
        rfcomm.execCommand("plclear");
    }

    /**
     * Let PyBlaster jump to tune in playlist
     */
    function jump_to_tune(position) {
        rfcomm.execCommand("plgoto "+position);
    }


    /**
     * Set all items to inactive to disable highlighted item
     */
    function set_all_inactive() {
        for ( var i = 0; i < count; i++ ) {
            get(i).active = false;
        }
    }

    /**
     * Triggered by main if playstatus received.
     * Set all items to inactive and highlight currently played item.
     */
    function gotPlayStatus(msg) {
        if ( msg.status() != 0 ) {
            set_all_inactive();
        } else {
            var arr = msg.payloadElements(0);
            var pos = arr[11];
            for ( var i = 0; i < count; i++ ) {
                get(i).active = ( get(i).position == pos );
            }
        }
    }


    /**
     * Called by main if shwowdevices message received from PI
     */
    function received_playlist(msg) {
        clearAll();

        var nowIndex = -1
        if ( msg.status() == 0 ) {
            for ( var i = 0; i < msg.payloadSize(); i++ ) {
                var arr = msg.payloadElements(i);
                append({"position": arr[0],
                        "state": arr[1],
                        "title": arr[2],
                        "active": ( arr[1] == "2" ),
                        "selected": false
                       });
                if ( arr[1] == "2" ) nowIndex = i;
            }
        } else {
            root.log_error("Bad return status for 'plshow'");
        }

        if ( nowIndex != -1 ) {
            positionViewAtIndex(nowIndex, ListView.Center)
        }
    }

    /**
     * Invoke playlist modify function
     * Args:
     *  - 1: clear
     *  - 2: after current
     *  - 3: to end
     */
    function modify_playlist(mod_mode)
    {
        console.log("modify_playlist("+mod_mode+") called.");

        rfcomm.clearSendPayload();

        for ( var i = 0; i < count; i++ )
        {
            var elem = get(i);
            if ( elem.selected )
            {
                rfcomm.addToSendPayload("POD "+elem.position);
            }
        }

        deselect_all();

        rfcomm.execCommandWithPayload("plmodify "+mod_mode);
    }

    /**
     * Randomize current playlist
     * mode 1 -- all
     * mode 2 -- after current position
     */
    function randomize(mode) {
        if ( mode == 1 ) {
            rfcomm.execCommand("plrandomize 1");
        } else if ( mode == 2 ) {
            rfcomm.execCommand("plrandomize 2");
        }
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

