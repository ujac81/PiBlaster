"""usbscan.py check /proc/mounts for newly attached usb devices


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import log
import time

from usbdevice import UsbDevice


class UsbManager:
  """ Includes poll function check_new_usb() and holds usbdevice instances for each active usb device
  """

  def __init__(self, parent):
    """
    """
    self.parent         = parent
    self.usbdevs        = []      # list of active USB devices
    self.invaliddevs    = []      # list of [dev,mnt_pnt] combinations that have been found as invalid
    self.alldevs        = {}      # list of all attaches storage ids (storid: usbdevice)


  def check_new_usb(self):
    """ poll function, will check for new usb devices and create new usbdevice instances or delete lost usbdevice instances
    """

    f = open("/proc/self/mounts", "r")

    usb_mounts = []

    # find available usb by mount point
    for line in f:
      dev, mnt_pnt = line.split()[:2]
      if self.invaliddevs.count([dev, mnt_pnt]) == 0  and mnt_pnt.count("/media/usb") > 0:
        usb_mounts.append(mnt_pnt)
        # if new usb found
      # for line /proc/mounts

    # check new usb found
    for item in usb_mounts:
      if not self.has_usb_stor(item):
        # new usb storage --> generate
        self.new_usb_stor(item)

    # check usb lost
    for item in self.usbdevs:
      if usb_mounts.count(item.mnt_pnt) == 0:
        # lost usb device --> remove MP3s from list
        self.remove_usb_stor(item.mnt_pnt)

    # end check_new_usb() #



  def has_usb_stor(self, mnt_pnt):
    """ Check if we have usbdevice for mount point mnt_pnt
    """
    for stor in self.usbdevs:
      if stor.mnt_pnt == mnt_pnt:
        return True
    return False

    # end has_usb_stor() #


  def has_usb_dev(self, dev):
    """ Check if we have usbdevice for device
    """
    for stor in self.usbdevs:
      if stor.dev == dev:
        return True
    return False

    # end has_usb_stor() #



  def new_usb_stor(self, mnt_pnt):
    """ Create new UsbDevice instance which will start scanning in init
    """

    newstor = UsbDevice(self, mnt_pnt)

    if not newstor.valid:
      self.parent.log.write(log.MESSAGE, "Skipping new USB device at %s because of double insertion or missing device node" % mnt_pnt)
      self.invaliddevs.append([newstor.dev, newstor.mnt_pnt])
      return

    self.usbdevs.append(newstor)
    self.alldevs[newstor.storid] = newstor

    # end new_usb_stor() #



  def remove_usb_stor(self, mnt_pnt):
    """ Remove usb storage -- all file entries will die with usbdevice instance
    """

    for i in range(len(self.usbdevs)):
      if self.usbdevs[i].mnt_pnt == mnt_pnt:
        self.parent.log.write(log.DEBUG1, "[USBMANAGER] delete usbdev id %d for %s " % (self.usbdevs[i].storid, mnt_pnt))
        self.usbdevs[i].release()

        # remove from lists
        del self.alldevs[self.usbdevs[i].storid]
        del self.usbdevs[i]

        return

    self.parent.log.write(log.EMERGENCY, "FileManager.remove_usb_stor() Tried to remove %s but no such device found!" % mnt_pnt)
    raise Exception("no such device %s to remove" % mnt_pnt)

    # end remove_usb_stor() #



  def get_dev_by_strid(self, strid):
    """ Save get usbdevice instance from storage id string

    Returns None if bad string or if no such storage
    """
    if not strid: return None

    try:
      storid = int(strid)
    except TypeError:
      return None
    except ValueError:
      return None

    if not storid in self.alldevs: return None

    return self.alldevs[storid]

    # end get_dev_by_strid() #


  def rescan_usb_stor(self, strid):
    """Drop USB device, drop all DB entries for this device and rescan it

    return 0: no such dev
    return 1: device rescaned
    """

    usbdev = self.get_dev_by_strid(strid)
    if not usbdev: return 0

    mnt_pnt = usbdev.mnt_pnt
    devid   = usbdev.storid
    self.remove_usb_stor(usbdev.mnt_pnt)
    self.parent.dbhandle.invalidate_md5(devid)
    self.new_usb_stor(mnt_pnt)

    return 1

    # end rescan_usb_stor() #






