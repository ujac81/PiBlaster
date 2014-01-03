
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

# Add more folders to ship with the application, here
folder_01.source = qml/PiBlaster
folder_01.target = qml
DEPLOYMENTFOLDERS = folder_01

# Additional import path used to resolve QML modules in Creator's code model
QML_IMPORT_PATH =


SOURCES += src/main.cpp \
    src/RFCommClient.cpp
HEADERS += \
    src/RFCommClient.h

RESOURCES += images.qrc

! contains(DUMMY_MODE, 1) {
    OTHER_FILES += \
        android-sources/src/org/piblaster/piblaster/rfcomm/RfcommClient.java \
        android-sources/AndroidManifest.xml
}

# Please do not modify the following two lines. Required for deployment.
include(src/QtQuick2ApplicationViewer.pri)
qtcAddDeployment()




