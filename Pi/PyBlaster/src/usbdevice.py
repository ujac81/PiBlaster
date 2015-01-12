"""usbstor.py -- Contains data for one single usb storage device


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import mad
import md5
import os
import subprocess
import time
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from dirscanner import DirScanner
import log
from helpers import seconds_to_minutes


class UsbDevice:
    """Contains data for one single usb storage device

    Handled by UsbManager.
    """

    def __init__(self, parent, mnt_pnt):
        """Will fully initialize everything for this usb drive.

        Check if data for this stick found in database, otherwise rebuild and
        insert data into database.
        """

        self.parent = parent
        self.main = parent.parent
        self.mnt_pnt = mnt_pnt
        self.label = None
        self.uuid = None
        self.alias = None
        self.dev = None
        self.revision = 0
        self.valid = True
        self.totsubdirs = 0
        self.totfiles = 0
        self.cur_tot_bytes = 0
        self.bytes_free = 0

        # Get dev entry for mnt_pnt.
        f = open("/proc/mounts", "r")
        for line in f:
            toks = line.split()
            if toks[1] == mnt_pnt:
                self.dev = toks[0]

        if self.dev is None:
            # No device found, we assume that this is a local dir.
            # Set device name to directory name
            self.dev = mnt_pnt

        # Check that no other instance exists for this device.
        # (should not happen, but PI sometimes boots with strange mtab entries)
        if self.parent.has_usb_dev(self.dev):
            self.valid = False
            return

        # Check if we have device entry for dev.
        # (should be, but PI sometimes has obsolete entries in mounts....)
        if not os.path.exists(self.dev):
            self.valid = False
            return

        # Try to find label for usb device.
        for line in subprocess.check_output(['blkid']).split('\n'):
            if line.startswith(self.dev):
                for item in line.split(' '):
                    toks = item.split('=')
                    if toks[0] == "LABEL":
                        self.label = toks[1].strip('"')
                    if toks[0] == "UUID":
                        self.uuid = toks[1].strip('"')

        # If local directory set label and uuid to dirname.
        if self.label is None:
            self.label = mnt_pnt
        if self.uuid is None:
            self.uuid = mnt_pnt

        # Get storid and alias from database, if no alias found, use label.
        self.storid, self.alias, self.revision = \
            self.main.dbhandle.get_usbid(self.uuid)
        if not self.label:
            self.label = "usbdev%d" % self.storid
        if self.alias is None:
            self.alias = self.label

        # Found new usb device --> scan for MP3s.
        self.main.log.write(log.MESSAGE, "Found new USB device %s with label "
                                         "%s mounted at %s as id %d using "
                                         "alias %s" % (self.dev,
                                                       self.label,
                                                       self.mnt_pnt,
                                                       self.storid,
                                                       self.alias))

        # Flash load led.
        self.main.led.set_led_yellow(1)

        # Create md5 of os.walk() to check if we know this stick.
        m = md5.new()
        for root, dirs, files in os.walk(mnt_pnt):
            # Do not add root here as it contains mount point, which may
            # change and result in a different md5 hash.
            m.update("%s%s" % (''.join(dirs), ''.join(files)))
        digest = m.hexdigest()

        self.main.log.write(log.MESSAGE, "Got md5 %s for dir structure on "
                                         "USB stick with UUID %s" %
                                         (digest, self.uuid))

        # Check if we know this stick, if yes load from db, otherwise scan it.

        if self.main.dbhandle.add_or_update_usb_stor(self.storid,
                                                     self.uuid, digest):
            # Run from DB

            self.main.dbhandle.cur.execute(
                "SELECT COUNT(id) FROM Dirs WHERE usbid=?;", (self.storid,))
            self.totsubdirs = self.main.dbhandle.cur.fetchone()[0]

            self.main.dbhandle.cur.execute(
                "SELECT COUNT(id) FROM Fileentries WHERE usbid=?;",
                (self.storid,))
            self.totfiles = self.main.dbhandle.cur.fetchone()[0]

            self.main.dbhandle.cur.execute(
                "SELECT bytesfree, bytesused FROM Usbdevs WHERE id=?;",
                (self.storid,))
            row = self.main.dbhandle.cur.fetchone()
            self.bytes_free = row[0]
            self.cur_tot_bytes = row[1]

            self.main.log.write(log.MESSAGE, "done reloading from db in %s, "
                                             "total %d dirs found, including "
                                             "%d files in revision %d." %
                                             (self.dev, self.totsubdirs,
                                              self.totfiles, self.revision))

        else:
            start = time.clock()

            self.cur_dir_id = 0
            self.cur_tot_bytes = 0

            scanner = DirScanner(self, mnt_pnt, self.storid)
            scanner.scan()

            stat_usb = os.statvfs(mnt_pnt)
            self.bytes_free = stat_usb.f_frsize * stat_usb.f_bavail

            self.main.dbhandle.con.commit()

            self.main.dbhandle.cur.\
                execute("SELECT COUNT(id) FROM Dirs WHERE usbid=?;",
                        (self.storid,))
            self.totsubdirs = self.main.dbhandle.cur.fetchone()[0]

            self.main.dbhandle.cur.\
                execute("SELECT COUNT(id) FROM Fileentries WHERE usbid=?;",
                        (self.storid,))
            self.totfiles = self.main.dbhandle.cur.fetchone()[0]

            elapsed = time.clock() - start
            self.main.log.write(log.MESSAGE, "done scanning in %s, total %d "
                                             "dirs found, including %d files."
                                             " Took %fs" %
                                             (self.dev, self.totsubdirs,
                                              self.totfiles, elapsed))

            # Tell db that scan is ok now.
            self.revision += 1
            self.main.dbhandle.set_scan_ok(self.storid, self.revision,
                                           self.bytes_free, self.cur_tot_bytes)

            # else scan #

        # Unflash load led.
        self.main.led.set_led_yellow(0)

        # Tell playlist to check if items may be enabled or
        # if revisions have changed.
        self.main.listmngr.usb_connected(self.storid, self.revision, self)

        # end __init__() #

    def release(self):
        """Called if device node for this stick is lost.

        Remove entries from playlist.
        """
        self.main.log.write(log.MESSAGE, "Lost USB device %s" % self.mnt_pnt)
        self.main.listmngr.usb_removed(self.storid)

    def update_alias(self, alias):
        """Change alias for this USB dev via database"""

        if self.main.dbhandle.update_alias(self.storid, alias):
            self.alias = alias
            return True
        return False

    def list_all_dirs(self):
        """Called by 'lsalldirs <storid>' command

        :returns [[device-id,dir-id,num subdirs,num files,
                    full dir path incl mount point]]
        """

        ret = []
        for row in self.main.dbhandle.cur.\
                execute("SELECT id, numdirs, numfiles, dirname from Dirs "
                        "WHERE usbid=? ORDER BY id;", (self.storid,)):
            ret.append(['%d' % self.storid,
                        '%d' % row[0],
                        '%d' % row[1],
                        '%d' % row[2],
                        u'%s', row[3]])
        return ret

    def list_dirs(self, dirid):
        """Called by 'lsdirs <storid> <dirid>' command

        :returns [[device-id,dir-id,parent-id,num subdirs,num files,
                    full dir path incl mount point]]
        """
        if dirid is None:
            return []

        ret = []
        for row in self.main.dbhandle.cur.\
                execute("SELECT id, parentid, numdirs, numfiles, dirname, "
                        "path from Dirs WHERE usbid=? AND parentid=? ORDER "
                        "BY id;", (self.storid, dirid,)):
            ret.append(['%d' % self.storid,
                        '%d' % row[0],
                        '%d' % row[1],
                        '%d' % row[2],
                        '%d' % row[3],
                        u'%s' % row[4],
                        u'%s' % row[5]])
        return ret

    # end list_dirs() #

    def list_files(self, dirid):
        """

        :returns [[storid,dirid,fileid,length,artist,album,title]]
        """
        if dirid is None:
            return []

        ret = []
        for row in self.main.dbhandle.cur.\
                execute("SELECT id, time, artist, album, title FROM "
                        "Fileentries WHERE usbid=? AND dirid=? ORDER BY id;",
                        (self.storid, dirid,)):
            ret.append(['%d' % self.storid,
                        '%d' % dirid,
                        '%d' % row[0],
                        '%s' % seconds_to_minutes(row[1]),
                        row[2],
                        row[3],
                        row[4]])
        return ret

    # end list_dirs() #

    def list_full_dir(self, dirid):
        """Combined dir and file list for dirid.

        :returns [[1,device-id,dir-id,parent-id,num subdirs,num files,
                    full dir path incl mount point]] (dirs)
                 [[2,storid,dirid,fileid,length,artist,album,title]] (files)
        """
        ret = []
        dirs = self.list_dirs(dirid)
        for item in dirs:
            ret.append(["1"]+item)
        files = self.list_files(dirid)
        for item in files:
            ret.append(["2"]+item)
        return ret

    # end list_full_dir() #

    def get_fileentry_by_path(self, path):
        """
        """
        for row in self.main.dbhandle.cur.\
                execute("SELECT * FROM Fileentries WHERE usbid=? AND path=?",
                        (self.storid, path,)):
            return row

        return None
