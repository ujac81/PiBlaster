
QT += quick

DUMMY_MODE = 1

contains(DUMMY_MODE, 1) {
    message("Running in dummy mode")
    DEFINES += "DUMMY_MODE=1"
} else {
    message("Running in full android mode")
    QT += androidextras
    ANDROID_PACKAGE_SOURCE_DIR = $$PWD/android-sources
}


# Additional import path used to resolve QML modules in Creator's code model
QML_IMPORT_PATH =


SOURCES += src/main.cpp \
    src/RFCommClient.cpp \
    src/Helpers.cpp
HEADERS += \
    src/RFCommClient.h \
    src/Helpers.h

RESOURCES += images.qrc
RESOURCES += qml.qrc

! contains(DUMMY_MODE, 1) {
    OTHER_FILES += \
        android-sources/src/org/piblaster/piblaster/rfcomm/RfcommClient.java \
        android-sources/AndroidManifest.xml
}

# Please do not modify the following two lines. Required for deployment.
include(src/QtQuick2ApplicationViewer.pri)
qtcAddDeployment()
