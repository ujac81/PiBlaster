"""usbstor.py -- Contains data for one single usb storage device


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import md5
import os
import subprocess
import time

import log
from direntry import DirEntry
from fileentry import FileEntry

class UsbDevice:
  """Contains data for one single usb storage device

  Handled by UsbManager.
  """

  def __init__(self, parent, mnt_pnt):
    """Will fully initialize everything for this usb drive.

    Check if data for this stick found in database, otherwise rebuild and
    insert data into database.
    """

    self.parent         = parent
    self.main           = parent.parent
    self.mnt_pnt        = mnt_pnt
    self.label          = None
    self.dev            = None
    self.root_dir_entry = None
    self.cur_dir_id     = 0     # Will be increased while recursion in
                                # direntry.init walks through file tree.
    self.valid          = True
    self.totsubdirs     = 0
    self.totfiles       = 0
    self.alldirs        = {}    # (dirid, DirEntry) hash

    # Get dev entry for mnt_pnt.
    f = open("/proc/mounts", "r")
    for line in f:
      toks = line.split()
      if toks[1] == mnt_pnt:
        self.dev = toks[0]

    # Check that no other instance exists for this device.
    # (should not happen, but PI sometimes boots with strange mtab entries)
    if self.parent.has_usb_dev(self.dev):
      self.valid = False
      return

    # Check if we have device entry for dev.
    # (should be, but PI sometimes has obsolet entries in mounts....)
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
          if toks[0] == "UUID" :
            self.uuid  = toks[1].strip('"')

    self.storid = self.main.dbhandle.get_usbid(self.uuid)
    if not self.label:
      self.label = "usbdev%d" % self.storid

    # Found new usb device --> scan for MP3s.
    self.main.log.write(log.MESSAGE,
      "Found new USB device %s with label %s mounted at %s as id %d" %
      (self.dev, self.label, self.mnt_pnt, self.storid))

    # Flash load led.
    self.main.led.set_led_yellow(1)

    # Create md5 of os.walk() to check if we know this stick.
    m = md5.new()
    for root, dirs, files in os.walk(mnt_pnt):
      # Do not add root here as it contains mount point which may change
      # and result in a different md5 hash.
      m.update("%s%s" % (''.join(dirs), ''.join(files)))
    digest = m.hexdigest()

    self.main.log.write(log.MESSAGE,
      "Got md5 %s for dir structure on USB stick with UUID %s" %
      (digest, self.uuid))

    # Check if we know this stick, if yes load from db, otherwise scan it.

    if self.main.dbhandle.add_or_update_usb_stor(self.storid, self.uuid, digest):
      # Rebuild dir/file tree from database.

      start = time.clock()
      self.rebuild_from_db()
      elapsed = time.clock() - start
      self.main.log.write(log.MESSAGE, "done reloading from db in %s, total " \
        "%d dirs found, including %d files. Took %fs" %
        (self.dev, self.totsubdirs, self.totfiles, elapsed))

    else:
      # Rescan usb device. DirEntry constructor will invoke dir scanner.

      start = time.clock()
      self.root_dir_entry = DirEntry(root=self, directory=mnt_pnt)
      elapsed = time.clock() - start
      self.main.log.write(log.MESSAGE,
        "done scanning in %s, total %d dirs found, including %d files. " \
        "Took %fs" % (self.dev, self.totsubdirs, self.totfiles, elapsed))

      # This will cause recursive insertion into database.
      self.main.led.set_led_yellow(1)
      self.main.led.set_led_green(1)
      start = time.clock()
      self.root_dir_entry.db_insert()
      self.main.dbhandle.con.commit()
      elapsed = time.clock() - start
      self.main.log.write(log.MESSAGE, "done db insertion. Took %fs" % elapsed)
      self.main.led.set_led_yellow(0)
      self.main.led.set_led_green(0)

      # Tell db that scan is ok now.
      self.main.dbhandle.set_scan_ok(self.storid)

    # end __init__() #

  def release(self):
    """Called if device node for this stick is lost.

    Remove entries from playlist.
    """

    self.main.log.write(log.MESSAGE, "Lost USB device %s" % self.mnt_pnt)

  def rebuild_from_db(self):
    """Reinit dirs/files from database"""

    self.main.led.set_led_yellow(1)
    self.main.led.set_led_green(1)

    # Create root directory.
    self.root_dir_entry = DirEntry(root=self, directory=self.mnt_pnt,
                                   dbrebuild=True)
    self.totsubdirs = 1

    dirs = { 0 : self.root_dir_entry }
    self.alldirs[0] = self.root_dir_entry

    # 1st run to create dirs

    for dirrow in self.main.dbhandle.cur.execute(
        "SELECT * FROM Dirs WHERE usbid=?;", (self.storid,)):

      dirid     = dirrow[0]
      parentid  = dirrow[1]
      parent    = dirs[parentid]
      if not parent:
        raise Exception(
          'UsbDevice.rebuild_from_db(): parent dir not loaded so far!')

      directory = os.path.join(self.mnt_pnt, dirrow[3])

      newdir = DirEntry(root=self, directory=directory, parent=parent,
                        parentid=parentid, dbrebuild=True)
      newdir.dirid[1] = dirid

      parent.dirs.append(newdir)
      dirs[dirid]         = newdir
      self.alldirs[dirid] = newdir

      self.totsubdirs += 1

      # for dirrow in scan dirs #

    # Rerun all dirs and fill in files.

    for dirid, direntry in dirs.iteritems():
      for filerow in self.main.dbhandle.cur.execute(
          "SELECT * FROM Fileentries WHERE usbid=? AND dirid=?;",
          (self.storid, dirid)):

        # 0=id, 1=dirid, 2=usbid, 3=path, 4=filename, 5=extension,
        # 6=genre, 7=year, 8=title, 9=album, 10=artist, 11=length

        path = os.path.join(self.mnt_pnt, filerow[3])
        newfile = FileEntry(path, filerow[:3], dbrebuild=True)

        newfile.filename  = filerow[4]
        newfile.extension = filerow[5]
        newfile.GENRE     = filerow[6]
        newfile.YEAR      = filerow[7]
        newfile.TITLE     = filerow[8]
        newfile.ALBUM     = filerow[9]
        newfile.ARTIST    = filerow[10]
        newfile.length    = filerow[11]

        direntry.files.append(newfile)

        self.totfiles += 1

        # for filerow

      # for dirrow in scan files

    self.main.led.set_led_yellow(0)
    self.main.led.set_led_green(0)

    # end rebuild_from_db() #


  def list_all_dirs(self):
    """Called by 'lsalldirs <storid>' command

    Returns "||device-id||dir-id||num subdirs||num files||full dir path incl mount point||"
    """
    ret = []
    for key, d in self.alldirs.iteritems():
      ret.append("||%d||%d||%d||%d||%s||" %
                 (d.dirid[0], d.dirid[1], len(d.dirs), len(d.files),
                  d.directory))
    return ret

  def list_dirs(self, strdirid):
    """Called by 'lsdirs <storid> <dirid>' command

    Returns "||device-id||dir-id||num subdirs||num files||full dir path incl mount point||"
    """
    if not strdirid:
      return []

    try:
      dirid = int(strdirid)
    except TypeError:
      return []
    except ValueError:
      return []

    if not dirid in self.alldirs:
      return []

    ret = []
    for d in self.alldirs[dirid].dirs:
      ret.append("||%d||%d||%d||%d||%s||" %
                 (d.dirid[0], d.dirid[1], len(d.dirs), len(d.files),
                  d.directory))
    return ret

  # end list_dirs() #


  def list_files(self, strdirid):
    """
    """
    if not strdirid:
      return []

    try:
      dirid = int(strdirid)
    except TypeError:
      return []
    except ValueError:
      return []

    if not dirid in self.alldirs:
      return []

    ret = []
    for f in self.alldirs[dirid].files:
      ret.append(u'||%d||%d||%d||%d||%s||%s||%s||' %
                 (f.file_id[0], f.file_id[1], f.file_id[2], f.length,
                  f.ARTIST, f.ALBUM, f.TITLE))
    return ret

  # end list_dirs() #
