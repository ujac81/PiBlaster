import QtQuick 2.0

ListView {

    anchors.fill: parent
    clip: true

    model: SearchModel{}
    delegate: Rectangle {
        id: searchDelegate
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
                text: ""
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
                searchList.model.get(index).selected = ! searchList.model.get(index).selected
            }
        }
    }
}

