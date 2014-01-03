import QtQuick 2.0


ListModel {
    id: browseModel

    property int level: 0




    function clearAll() {
        clear();
    }


    function load(dir_id) {
        clearAll();

        if (dir_id == "root") {

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
                           })
                }
            } else {
                // TODO error -- disconnected?
            }
        } // subdir
    }

    function itemText(index) {
        if ( get(index).type == 0 ) {
            return '<table width="100%">
  <tr>
    <td colspan="4"><strong>'+get(index).name+'</strong></td>
  </tr>
  <tr>
    <td align="left" style="font-size: 14px;">free:</td>
    <td align="right" width="60px" style="font-size: 14px;">'+get(index).free+'</td>
    <td align="right" style="font-size: 14px;">dirs:</td>
    <td align="right" width="40px" style="font-size: 14px;">'+get(index).dirs+'</td>
  </tr>
  <tr>
    <td align="left" style="font-size: 14px;">used:</td>
    <td align="right" width="60px" style="font-size: 14px;">'+get(index).used+'</td>
    <td align="right" style="font-size: 14px;">files:</td>
    <td align="right" width="40px" style="font-size: 14px;">'+get(index).files+'</td>
  <tr>
</table>';
        } else if ( get(index).type == 1 ) {
            return '<table width="100%">
  <tr>
    <td colspan="2"><strong>'+get(index).name+'</strong></td>
  </tr>
  <tr>
    <td align="left" style="font-size: 14px;">sub dirs:</td>
    <td align="right" width="60px" style="font-size: 14px;">'+get(index).dirs+'</td>
  </tr>
  <tr>
    <td align="left" style="font-size: 14px;">files:</td>
    <td align="right" width="60px" style="font-size: 14px;">'+get(index).files+'</td>
  <tr>
</table>';

        } else if ( get(index).type == 2 ) {
            return '<table width="100%">
  <tr>
    <td colspan="2"><strong>'+get(index).title+'</strong></td>
  </tr>
  <tr>
    <td colspan="2" style="font-size: 14px;">'+get(index).album+'</td>
  </tr>
  <tr>
    <td style="font-size: 14px;">'+get(index).artist+'</td>
    <td align="right" style="font-size: 14px;">'+get(index).time+'</td>
  </tr>
</table>';

        }
    }



}

