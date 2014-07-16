#PiBlaster

Docs and source code for the PiBlaster project....

**To be completed...**


# Development Environment

## Installation of QtCreator 5.3 on unbuntu linux 14.04
Download Qt >= 5.31 online installer and run it
```
$ chmod 755 qt-opensource-linux-x64-1.6.0-4-online.run
$ sudo qt-opensource-linux-x64-1.6.0-4-online.run
```
and install it to any location (/opt/Qt) is okay.
Default selection of packages is ok, just make sure x86_64, armv7 are
selected for Qt and QtCreator is selected for tools.


# Set up Raspberry Pi

## Installation of latest Raspbian
See [installing images on linux](http://www.raspberrypi.org/documentation/installation/installing-images/linux.md)

#### Download
[Download](http://www.raspberrypi.org/downloads/) zip image for Raspbian (debian wheezy) and unzip it.

#### Write SD
Insert empty SD card and make sure its not mounted Check the device name of the inserted SD card
```
$ dmesg | tail
```
it should print some information about the last connected device or so.
You need the device name like [sdb] or [sdc]. Don't make an error here or you
might mess up one of your working devices!

Copy image to SD card:
```
$ sudo dd bs=4M if=2014-06-20-wheezy-raspbian.img of=/dev/sdX
```
put the device later instead of the last X

#### Boot Pi and upgrade
Place SD card into PI and connect LAN, monitor and keyboard. In the software configuration select
* Expand Filesystem
* Advanced options -> ssh -> enable

and reboot. If connected via LAN you can now use ssh to connect to your PI.

Default password for user pi is *raspberry*.

To upgrade run
```
$ sudo aptitude update
$ sudo aptitude upgrade
```

#### Download and install PiBlaster software
You can download and create the piblaster package right on your PI, all you
need is cmake
```
$ sudo aptitude install cmake
```
No clone the git repo


sudo dpkg -i --force-depends /tmp/pyblaster-0.2.6-armhf.deb
sudo aptitude install -f
python-bluez python-mutagen python-sqlite python-rpi.gpio sqlite3 bluez python-lirc

/etc/modules
lirc_dev
lirc_rpi gpio_in_pin=25


vim /etc/lirc/hardware.conf
# /etc/lirc/hardware.conf
#
# Arguments which will be used when launching lircd
LIRCD_ARGS=""

# Don't start lircmd even if there seems to be a good config file
# START_LIRCMD=false

# Don't start irexec, even if a good config file seems to exist.
# START_IREXEC=false

# Try to load appropriate kernel modules
LOAD_MODULES=true

# Run "lircd --driver=help" for a list of supported drivers.
DRIVER="default"
# usually /dev/lirc0 is the correct setting for systems using udev
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"

# Default configuration files for your hardware if any
LIRCD_CONF=""
LIRCMD_CONF=""


/etc/lirc/lircd.conf
# Please make this file available to others
# by sending it to <lirc@bartelmus.de>
#
# this config file was automatically generated
# using lirc-0.9.0-pre1(default) on Tue Oct  8 07:05:38 2013
#
# contributed by
#
# brand:                       /home/pi/lircd.conf
# model no. of remote control:
# devices being controlled by this remote:
#

begin remote

  name  /home/pi/lircd.conf
  bits           16
  flags SPACE_ENC|CONST_LENGTH
  eps            30
  aeps          100

  header       9006  4447
  one           594  1648
  zero          594   526
  ptrail        587
  repeat       9006  2210
  pre_data_bits   16
  pre_data       0xFD
  gap          107633
  toggle_bit_mask 0x0

      begin codes
          KEY_1                    0x08F7
          KEY_2                    0x8877
          KEY_3                    0x48B7
          KEY_4                    0x28D7
          KEY_5                    0xA857
          KEY_6                    0x6897
          KEY_7                    0x18E7
          KEY_8                    0x9867
          KEY_9                    0x58A7
          KEY_0                    0x30CF
          KEY_DOWN                 0xB04F
          KEY_LEFT                 0x10EF
          KEY_UP                   0xA05F
          KEY_RIGHT                0x50AF
          KEY_BACK                 0x708F
          KEY_ENTER                0x906F
          KEY_SETUP                0x20DF
          KEY_PAUSE                0x609F
          KEY_PAUSE                0x807F
          KEY_STOP                 0x609F
          KEY_VOLUMEUP             0x40BF
          KEY_VOLUMEDOWN           0x00FF
      end codes

end remote

/root/.lircrc



begin
  button = KEY_PAUSE
  prog = pyblaster
  config = playpause
end



begin
  button = KEY_UP
  prog = pyblaster
  config = playprev
end



begin
  button = KEY_DOWN
  prog = pyblaster
  config = playnext
end

begin
  button = KEY_VOLUMEUP
  prog = pyblaster
  config = volinc
  repeat = 2
end

begin
  button = KEY_VOLUMEDOWN
  prog = pyblaster
  config = voldec
  repeat = 2
end
