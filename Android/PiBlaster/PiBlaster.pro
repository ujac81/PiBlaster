
QT += quick

DUMMY_MODE = 0

contains(DUMMY_MODE, 1) {
    message("Running in dummy mode")
    DEFINES += "DUMMY_MODE=1"
} else {
    message("Running in full android mode")
    QT += androidextras
    ANDROID_PACKAGE_SOURCE_DIR = $$PWD/android-sources
}

SOURCES += src/main.cpp \
    src/RFCommSendThread.cpp \
    src/RFCommRecvThread.cpp \
    src/RFCommMaster.cpp
HEADERS += \
    src/RFCommSendThread.h \
    src/RFCommMessageObject.h \
    src/RFCommRecvThread.h \
    src/RFCommMaster.h

contains(DUMMY_MODE, 1) {
    SOURCES += src/DummyMessages.cpp
}

RESOURCES += images.qrc
RESOURCES += qml.qrc

! contains(DUMMY_MODE, 1) {
    OTHER_FILES += \
        android-sources/src/org/piblaster/piblaster/rfcomm/RfcommClient.java \
        android-sources/AndroidManifest.xml
}

# Required for deployment
include(src/QtQuick2ApplicationViewer.pri)
qtcAddDeployment()

OTHER_FILES += \
    qml/PiBlaster/main.qml \
    qml/PiBlaster/tabview/TabView.qml \
    qml/PiBlaster/tabview/TabbedUI.qml \
    qml/PiBlaster/settings/Settings.qml \
    qml/PiBlaster/search/Search.qml \
    qml/PiBlaster/playlist/Playlist.qml \
    qml/PiBlaster/log/Log.qml \
    qml/PiBlaster/items/WaitOverlay.qml \
    qml/PiBlaster/items/Tab.qml \
    qml/PiBlaster/items/MessageWindow.qml \
    qml/PiBlaster/items/LineInput.qml \
    qml/PiBlaster/items/ButtonBox.qml \
    qml/PiBlaster/items/Button.qml \
    qml/PiBlaster/connect/Connect.qml \
    qml/PiBlaster/browse/BrowseModel.qml \
    qml/PiBlaster/browse/BrowseList.qml \
    qml/PiBlaster/browse/Browse.qml \
    qml/PiBlaster/play/Play.qml \
    qml/PiBlaster/playlist/PlayListModel.qml \
    qml/PiBlaster/playlist/PlayListList.qml
