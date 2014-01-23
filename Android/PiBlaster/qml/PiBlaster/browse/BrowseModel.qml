import QtQuick 2.0


ListModel {
    id: browseModel

    property var parentDir: new Array()

    function clearAll() {
        clear();
    }


    function dir_up() {

        console.log(parentDir);
        if (parentDir.length > 1) {
            parentDir.pop();
            load(parentDir[parentDir.length-1]);
        }
    }


    function load(dir_id) {
        clearAll();

        // prevent doublets in parent dir list
        if ( dir_id != parentDir[parentDir.length-1] )
            parentDir.push(dir_id)

        if (dir_id == "root") {

            parentDir = ["root"];

            var status = rfcommClient.execCommand("showdevices");

            if ( status == 0 )
            {
                for ( var i = 0; i < rfcommClient.numResults(); i++ )
                {
                    var arr = rfcommClient.result(i);
                    append({"type": 0,
                            "storid": arr[1],
                            "name": arr[3],
                            "files": arr[6],
                            "dirs": arr[5],
                            "free": arr[7],
                            "used": arr[8],
                            "dirid": "",    // dummy values for all possible fields required
                            "fileid": "",
                            "time": "",
                            "artist": "",
                            "album": "",
                            "title": "",
                            "selected": false,
                           })
                }
            } else {
                // TODO error -- disconnected?
            }
        // dir = root
        } else {
            var status = rfcommClient.execCommand("lsdirs "+dir_id);
            if ( status == 0 ) {
                for ( var i = 0; i < rfcommClient.numResults(); i++ )
                {
                    var arr = rfcommClient.result(i);
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
                           })
                }
            } else {
                // TODO error -- disconnected?
            }
            status = rfcommClient.execCommand("lsfiles "+dir_id);
            if ( status == 0 ) {
                for ( var i = 0; i < rfcommClient.numResults(); i++ )
                {
                    var arr = rfcommClient.result(i);
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
            } else {
                // TODO error -- disconnected?
            }
        } // subdir
    }

    function checkAnyThingSelected() {
        for ( var i = 0; i < count; i++ ) {
            if ( get(i).selected ) return true;
        }
        return false;
    }


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

        rfcommClient.preparePlaylistAdd(add_mode);

        for ( var i = 0; i < count; i++ )
        {
            var elem = get(i);
            if ( elem.selected )
            {
                if ( elem.type == 1 )
                    rfcommClient.addPlaylistItem("DIR "+elem.storid+" "+elem.dirid);
                else if ( elem.type == 2 )
                    rfcommClient.addPlaylistItem("FILE "+elem.storid+" "+elem.dirid+" "+elem.fileid);
            }
        }

        deselect_all();
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

