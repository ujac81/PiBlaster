import QtQuick 2.0

ListView {

    anchors.fill: parent
    clip: true

    model: BrowseModel{}
    delegate: Rectangle {
        id: browseDelegate
        width: parent.width
        height: root.baseFontSize * 3.8
        clip: true

        color: selected ? root.colorSelected : (index % 2 == 0 ? root.colorUnselected : root.colorUnselected2 )

        Row {
            width: parent.width
            // usb devices and folders get extra image column
            // media files (type == 2) do not get prefix
            Text {
                id: rowimg
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                text: if ( type == 0 )
                          '<img src="qrc:///images/images/usb.png" width="32px" height="32px"/>'
                      else if ( type == 1 )
                          '<img src="qrc:///images/images/folder.png" width="32px" height="32px"/>'
                      else
                          ""
                width: type < 2 ? 40 : 0
                verticalAlignment: Text.AlignBottom
            }
            // entry, content created via BrowseModel.itemText()
            Text {
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                anchors.left: rowimg.right
                textFormat: Text.RichText
                text: if ( index != -1 ) { // don't know why this might happen.
                          if ( type == 0 )
'<table width="100%">
<tr>
<td colspan="4"><strong>'+name+'</strong></td>
</tr>
<tr>
<td align="left" style="font-size: 14px;">free:</td>
<td align="right" width="60px" style="font-size: 14px;">'+free+'</td>
<td align="right" style="font-size: 14px;">dirs:</td>
<td align="right" width="40px" style="font-size: 14px;">'+dirs+'</td>
</tr>
<tr>
<td align="left" style="font-size: 14px;">used:</td>
<td align="right" width="60px" style="font-size: 14px;">'+used+'</td>
<td align="right" style="font-size: 14px;">files:</td>
<td align="right" width="40px" style="font-size: 14px;">'+files+'</td>
<tr>
</table>'
                          else if ( type == 1 )
'<table width="100%">
<tr>
<td colspan="2"><strong>'+name+'</strong></td>
</tr>
<tr>
<td align="left" style="font-size: 14px;">sub dirs:</td>
<td align="right" width="60px" style="font-size: 14px;">'+dirs+'</td>
</tr>
<tr>
<td align="left" style="font-size: 14px;">files:</td>
<td align="right" width="60px" style="font-size: 14px;">'+files+'</td>
<tr>
</table>'
                          else if ( type == 2 )
'<table width="100%">
<tr>
<td colspan="2"><strong>'+title+'</strong></td>
</tr>
<tr>
<td colspan="2" style="font-size: 14px;">'+album+'</td>
</tr>
<tr>
<td style="font-size: 14px;">'+artist+'</td>
<td align="right" style="font-size: 14px;">'+time+'</td>
</tr>
</table>'
                      } else
                          "ERROR BROKEN????"  // don't know why this might happen.
                font.pixelSize: root.baseFontSize
            }
        }

        MouseArea {
            id: elements_click_check
            anchors.fill: parent
            onClicked: {
                if ( browseList.model.get(index).type != 0 ) {
                    browseList.model.get(index).selected = ! browseList.model.get(index).selected
                }
            }
            onDoubleClicked: {
                var elem = browseList.model.get(index);
                if ( elem.type == 0 ) {
                    browseList.model.request_load(elem.storid+" 0", elem.name);
                } else if ( elem.type == 1 ) {
                    browseList.model.request_load(elem.storid+" "+elem.dirid, elem.name);
                }
            }
//            onPressAndHold: {
//                if ( browseList.model.get(index).type == 0 ) {
//                    browseList.model.load(browseList.model.get(index).storid+" 0");
//                } else if ( browseList.model.get(index).type == 1 ) {
//                    browseList.model.load(browseList.model.get(index).storid+" "+
//                                          browseList.model.get(index).dirid);
//                }
//            }
        }
    }
}

