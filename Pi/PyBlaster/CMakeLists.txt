

project(PyBlaster)
cmake_minimum_required(VERSION 2.8)

include(version.cmake)


add_subdirectory(src)
add_subdirectory(config)


set(CPACK_COMPONENTS_ALL_IN_ONE_PACKAGE 1)

set(CPACK_PACKAGE_NAME "pyblaster")
set(CPACK_PACKAGE_VENDOR "PiBlaster consortium")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Python daemon for the PiBlaster project")
set(CPACK_PACKAGE_VERSION ${PYBLASTER_VERSION_FULL})
set(CPACK_PACKAGE_VERSION_MAJOR ${PYBLASTER_VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR ${PYBLASTER_VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH ${PYBLASTER_VERSION_BUILD})
set(CPACK_SYSTEM_NAME "armhf")


set(CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Ulrich Jansen <ulrich.jansen@rwth-aachen.de>")
set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE armhf)
set(CPACK_DEBIAN_PACKAGE_VERSION ${PYBLASTER_VERSION_FULL})
set(CPACK_DEBIAN_PACKAGE_SECTION "devel")
set(CPACK_DEBIAN_PACKAGE_PRIORITY "extra")
set(CPACK_DEBIAN_PACKAGE_CONTROL_EXTRA "${CMAKE_CURRENT_SOURCE_DIR}/cmake/debian/postinst;${CMAKE_CURRENT_SOURCE_DIR}/cmake/debian/prerm;" )
set(CPACK_DEBIAN_PACKAGE_DEPENDS "udev, usbmount, python-bluez, python-mutagen, python-sqlite, python-rpi.gpio, sqlite3, bluez")


include(CPack)
