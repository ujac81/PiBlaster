"""usbscan.py -- Check /proc/mounts for newly attached usb devices

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import os

import log
from usbdevice import UsbDevice
from helpers import seconds_to_minutes


class UsbManager:
    """ Holds usbdevice instances for each active usb device

    Includes poll function check_new_usb().
    """

    def __init__(self, parent):
        """Set up empty device lists"""

        self.parent = parent
        self.usbdevs = []  # list of active USB devices
        self.invaliddevs = []  # list of [dev,mnt_pnt] combinations that
                               # have been found as invalid
        self.alldevs = {}  # list of all attaches storage ids
                           # (storid: usbdevice)

    def check_new_usb(self):
        """ Poll function, will check for new usb devices

        Create new usbdevice instances or delete lost usbdevice instances.
        """

        f = open("/proc/self/mounts", "r")

        usb_mounts = []

        # Find available usb by mount point.
        for line in f:
            dev, mnt_pnt = line.split()[:2]
            if self.invaliddevs.count([dev, mnt_pnt]) == 0 \
                    and mnt_pnt.count("/media/usb") > 0:
                usb_mounts.append(mnt_pnt)
        # add local dirs if found
        for localdir in self.parent.settings.localdirs:
            if os.path.exists(localdir):
                usb_mounts.append(localdir)

        # Check if new usb found.
        for item in usb_mounts:
            if not self.has_usb_stor(item):
                # Got new usb storage --> generate.
                self.new_usb_stor(item)

        # Check if usb lost.
        for item in self.usbdevs:
            if usb_mounts.count(item.mnt_pnt) == 0:
                # Lost usb device --> remove MP3s from list.
                self.remove_usb_stor(item.mnt_pnt)

        # Check local directories from config
        for localdir in self.parent.settings.localdirs:
            if not self.has_usb_stor(localdir):
                # manage local directories like usb devices -- should work
                self.new_usb_stor(localdir)

        # end check_new_usb() #

    def has_usb_stor(self, mnt_pnt):
        """ Check if we have usbdevice for mount point mnt_pnt"""

        for stor in self.usbdevs:
            if stor.mnt_pnt == mnt_pnt:
                return True
        return False

        # end has_usb_stor() #

    def has_usb_dev(self, dev):
        """ Check if we have usbdevice for device"""

        for stor in self.usbdevs:
            if stor.dev == dev:
                return True
        return False

        # end has_usb_stor() #

    def new_usb_stor(self, mnt_pnt):
        """ Create new UsbDevice instance which will start scanning in init"""

        newstor = UsbDevice(self, mnt_pnt)

        if not newstor.valid:
            self.parent.log.write(log.MESSAGE, "Skipping new USB device at "
                                               "%s because of double "
                                               "insertion or missing device "
                                               "node" % mnt_pnt)
            self.invaliddevs.append([newstor.dev, newstor.mnt_pnt])
            return

        self.usbdevs.append(newstor)
        self.alldevs[newstor.storid] = newstor

        # end new_usb_stor() #

    def remove_usb_stor(self, mnt_pnt):
        """Remove usb storage.

        All file entries will die with usbdevice instance
        """

        for i in range(len(self.usbdevs)):
            if self.usbdevs[i].mnt_pnt == mnt_pnt:
                self.parent.log.write(log.DEBUG1, "[USBMANAGER] delete "
                                                  "usbdev id %d for %s " %
                                                  (self.usbdevs[i].storid,
                                                   mnt_pnt))
                self.usbdevs[i].release()

                # remove from lists
                del self.alldevs[self.usbdevs[i].storid]
                del self.usbdevs[i]

                return

        self.parent.log.write(log.EMERGENCY, "FileManager.remove_usb_stor() "
                                             "Tried to remove %s but no such "
                                             "device found!" % mnt_pnt)
        raise Exception("no such device %s to remove" % mnt_pnt)

        # end remove_usb_stor() #

    def get_dev_by_storid(self, storid):
        """Save get usbdevice instance from storage id string

        Returns None if bad string or if no such storage.
        """

        if storid is None:
            return None

        if not storid in self.alldevs:
            return None

        return self.alldevs[storid]

        # end get_dev_by_strid() #

    def rescan_usb_stor(self, storid):
        """Drop USB device, drop all DB entries for this device and rescan it

        return 0: no such dev
        return 1: device rescaned
        """

        usbdev = self.get_dev_by_storid(storid)
        if usbdev is None:
            return 0

        mnt_pnt = usbdev.mnt_pnt
        devid = usbdev.storid
        self.remove_usb_stor(usbdev.mnt_pnt)
        self.parent.dbhandle.invalidate_md5(devid)
        self.new_usb_stor(mnt_pnt)

        return 1

        # end rescan_usb_stor() #

    def is_connected(self, storid):
        """Returns True if usb device with id storid is attached"""

        return storid in self.alldevs

    def revision(self, storid):
        """Get revision number of file tree for device storid

        Return -1 if no such storid
        """

        res = -1

        for row in self.parent.dbhandle.cur.execute(
                "SELECT revision FROM Usbdevs WHERE id=?", (storid,)):
            res = row[0]

        return res

    def connected_usbids(self):
        """Get list of connected storage ids"""
        return self.alldevs.keys()

    def search_files(self, pattern, mode=1, limit=200):
        """Search file entries for connected USB devices.

        :param pattern: search pattern for SQL (LIKE %pattern%)
        :param mode: 1=all fields, 2=title field
        :param limit: limit results count
        :returns [[usbid, dirid, fileid, time, artist, album, title, path]]
        """

        # unknown mode
        if mode not in [1, 2]:
            return []

        # available usb devs
        connected_usbs = self.connected_usbids()
        if not connected_usbs:
            return []

        usb_list = ",".join(map(str, connected_usbs))

        statement = "SELECT a.usbid, a.dirid, a.id, a.time, a.artist, " \
                    "a.album, a.title, b.alias, a.path FROM Fileentries AS " \
                    "a, Usbdevs AS b "
        if mode == 1:
            statement += "WHERE (a.artist {0:s} OR a.album {0:s} OR a.title " \
                         "{0:s} OR a.path {0:s})".\
                format("LIKE '%" + pattern + "%'")
        if mode == 2:
            statement += "WHERE a.title LIKE '%" + pattern + "%'"

        statement += " AND a.usbid IN (%s)" % usb_list
        statement += " AND a.usbid = b.id"
        statement += " ORDER BY a.usbid,a.dirid,a.id"
        statement += " LIMIT %d" % limit

        self.parent.log.write(log.DEBUG1, statement)

        ret = []

        for row in self.parent.dbhandle.cur.execute(statement):
            ret.append(['%d' % row[0],
                        '%d' % row[1],
                        '%d' % row[2],
                        '%s' % seconds_to_minutes(row[3]),
                        row[4],
                        row[5],
                        row[6],
                        row[7] + "/" + '/'.join(row[8].split('/')[:-1])])

        return ret
