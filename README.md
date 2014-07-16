#PiBlaster

Docs and source code for the PiBlaster project....

**To be completed...**


# Development Environment

## Installation of QtCreator 5.3 on unbuntu linux 14.04

* Download Qt >= 5.31 online installer and run it

    $ chmod 755 qt-opensource-linux-x64-1.6.0-4-online.run
    $ sudo qt-opensource-linux-x64-1.6.0-4-online.run

and install it to any location (/opt/Qt) is okay.
Default selection of packages is ok, just make sure x86_64, armv7 are
selected for Qt and QtCreator is selected for tools.


# Set up Raspberry Pi

## Installation of latest Raspbian
See [installing images on linux(http://www.raspberrypi.org/documentation/installation/installing-images/linux.md)
* Download zip image for Raspbian (debian wheezy) from

    http://www.raspberrypi.org/downloads/

and unzip it.
* Insert empty SD card and make sure its not mounted.
* Check the device name of the inserted SD card

    $ dmesg | tail

    it should print some information about the last connected device or so.
You need the device name like [sdb] or [sdc]. Don't make an error here or you
might mess up one of your working devices!
* Copy image to SD card:

    $ sudo dd bs=4M if=2014-06-20-wheezy-raspbian.img of=/dev/sdX

put the device later instead of the last X

