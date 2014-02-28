import QtQuick 2.0


ListModel {
    id: browseModel

    property var parentDir: new Array()
    property var parentPath: new Array()

    signal pathChanged(string path)


    function clearAll() {
        clear();
    }

    function dir_up() {
        if (parentDir.length > 1) {
            parentDir.pop();
            parentPath.pop();
            request_load(parentDir[parentDir.length-1], "");
        }
    }

    function on_root_dir() {
        if (parentDir.length <= 1)
            return true;
        return false;
    }


    /**
     * Send browse request to PyBlaster
     * Answer will be received by RFCommRecvThread and will be received
     * as QT signal.
     *
     */
    function request_load(dir_id, dir_name) {

        clearAll(); // delete already upon request to prevent mutiple request while user should wait.

        // prevent doublets in parent dir list
        if ( dir_id != parentDir[parentDir.length-1] ) {
            parentDir.push(dir_id);
            if ( dir_name != "" ) parentPath.push(dir_name);
        }

        if (dir_id == "root") {
            parentDir = ["root"];
            parentPath = [];
            var status = rfcomm.execCommand("showdevices");
        } else {
            rfcomm.execCommand("lsfulldir "+dir_id);
        }

        if ( parentPath.length == 0 ) {
            browseModel.pathChanged("root");
        } else {
            browseModel.pathChanged(parentPath.join("/"));
        }

    }

    /**
     * Called by main if shwowdevices message received from PI
     */
    function received_devices(msg) {
        clearAll();

        if ( msg.status() == 0 ) {
            for ( var i = 0; i < msg.payloadSize(); i++ ) {
                var arr = msg.payloadElements(i);
                append({"type": 0,
                        "storid": arr[0],
                        "name": arr[2],
                        "files": arr[5],
                        "dirs": arr[4],
                        "free": arr[6],
                        "used": arr[7],
                        "dirid": "",    // dummy values for all possible fields required
                        "fileid": "",
                        "time": "",
                        "artist": "",
                        "album": "",
                        "title": "",
                        "selected": false,
                       });
            }
        } else {
            root.log_error("Bad return status for 'showdevices'");
        }
    }


    /**
     * Called by main if lsfulldir message received from PI
     */
    function received_dir(msg) {
        clearAll();
        if ( msg.status() == 0 ) {
            for ( var i = 0; i < msg.payloadSize(); i++ ) {
                var arr = msg.payloadElements(i);
                if ( arr[0] == "1") {
                    append({"type": 1,
                            "storid": arr[1],
                            "dirid": arr[2],
                            "parentid": arr[3],
                            "dirs": arr[4],
                            "files": arr[5],
                            "name": arr[6],
                            "fileid": "", // dummy values for all possible fields required
                            "time": "",
                            "artist": "",
                            "album": "",
                            "title": "",
                            "selected": false,
                           });
                } else if ( arr[0] == "2" ) {
                    append({"type": 2,
                            "storid": arr[1],
                            "dirid": arr[2],
                            "fileid": arr[3],
                            "time": arr[4],
                            "artist": arr[5],
                            "album": arr[6],
                            "title": arr[7],
                            "selected": false,
                            });
                }
            }
        } else {
            root.log_error("Bad return status for 'lsfulldir'");
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
     * True if directories selected (ask if should be inserted)
     */
    function checkDirsInSelection() {
        for ( var i = 0; i < count; i++ ) {
            var elem = get(i);
            if ( elem.selected && elem.type == 1 ) return true;
            if ( elem.type == 2 ) return false; // dirs are on top, so no dirs more now
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
                if ( elem.type == 1 )
                    rfcomm.addToSendPayload("DIR "+elem.storid+" "+elem.dirid);
                else if ( elem.type == 2 )
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

