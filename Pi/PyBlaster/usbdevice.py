"""usbstor.py contains data for one single usb storage device found by usbmanger


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""


import subprocess
import os
import md5
import time

import log
from direntry import DirEntry
from fileentry import FileEntry

class UsbDevice:
  """
  """

  def __init__(self, parent, mnt_pnt):
    """
    """

    self.parent         = parent
    self.main           = parent.parent
    self.mnt_pnt        = mnt_pnt
    self.label          = None
    self.dev            = None
    self.root_dir_entry = None
    self.cur_dir_id     = 1     # will be increased will recursion in direntry.init walks through file tree
    self.valid          = True
    self.totsubdirs     = 0
    self.totfiles       = 0
    self.alldirs        = {}    # (dirid, DirEntry) hash

    # get dev entry for mnt_pnt
    f = open("/proc/mounts", "r")
    for line in f:
      toks = line.split()
      if toks[1] == mnt_pnt:
        self.dev = toks[0]

    # check that no other instance exists for this device
    # (should not happen, but PI sometimes boots with strange mtab entries)
    if self.parent.has_usb_dev(self.dev):
      self.valid = False
      return

    # check if we have device entry for dev
    # (should be, but PI sometimes has obsolet entries in mounts....)
    if not os.path.exists(self.dev):
      self.valid = False
      return

    # try to find label for usb device
    for line in subprocess.check_output(['blkid']).split('\n'):
      if line.startswith(self.dev):
        for item in line.split(' '):
          toks = item.split('=')
          if toks[0] == "LABEL": self.label = toks[1]
          if toks[0] == "UUID" : self.uuid  = toks[1]


    self.storid = self.main.dbhandle.get_usbid(self.uuid)
    if not self.label: self.label = "usbdev%d" % self.storid

    # found new usb device --> scan for MP3s
    self.main.log.write(log.MESSAGE, "Found new USB device %s with label %s mounted at %s as id %d" % (self.dev, self.label, self.mnt_pnt, self.storid))

    # flash load led
    self.main.led.set_led_yellow(1)

    # create md5 of os.walk to check if we know this stick
    m = md5.new()
    for root, dirs, files in os.walk(mnt_pnt):
      # do not add root here as it contains mount point which may change and result in a different md5 hash
      m.update("%s%s" % (''.join(dirs), ''.join(files)))
    digest = m.hexdigest()

    self.main.log.write(log.MESSAGE, "Got md5 %s for dir structure on USB stick with UUID %s" % (digest, self.uuid))


    # check if we know this stick, if yes rebuild from db, otherwise reread it

    if self.main.dbhandle.add_or_update_usb_stor(self.storid, self.uuid, digest):
      # rebuild dir/file tree from database

      start = time.clock()
      self.rebuild_from_db()
      elapsed = time.clock() - start
      self.main.log.write(log.MESSAGE, "done reloading from db in %s, total %d dirs found, including %d files. Took %fs" % (self.dev, self.totsubdirs, self.totfiles, elapsed))

    else:
      # rescan

      # this will invoke the dir scanner
      start = time.clock()
      self.root_dir_entry = DirEntry(root=self, directory=mnt_pnt)
      elapsed = time.clock() - start
      self.main.log.write(log.MESSAGE, "done scanning in %s, total %d dirs found, including %d files. Took %fs" % (self.dev, self.totsubdirs, self.totfiles, elapsed))

      # this will cause recursive insertion into database
      self.main.led.set_led_yellow(1)
      self.main.led.set_led_green(1)
      start = time.clock()
      self.root_dir_entry.db_insert()
      self.main.dbhandle.con.commit()
      elapsed = time.clock() - start
      self.main.log.write(log.MESSAGE, "done db insertion. Took %fs" % elapsed)
      self.main.led.set_led_yellow(0)
      self.main.led.set_led_green(0)

      # tell db that scan is ok now
      self.main.dbhandle.set_scan_ok(self.storid)

    # end __init__() #


  def release(self):
    """
    """
    self.main.log.write(log.MESSAGE, "Lost USB device %s" % self.mnt_pnt)


  def rebuild_from_db(self):
    """ Reinit dirs/files from db
    """

    self.main.led.set_led_yellow(1)
    self.main.led.set_led_green(1)

    # create root directory
    self.root_dir_entry = DirEntry(root=self, directory=self.mnt_pnt, dbrebuild=True)
    self.totsubdirs = 1

    dirs = { 1 : self.root_dir_entry }

    # 1st run to create dirs

    for dirrow in self.main.dbhandle.cur.execute("SELECT * FROM Dirs WHERE usbid=?;", (self.storid,)):

      dirid     = dirrow[0]
      parentid  = dirrow[1]
      parent    = dirs[parentid]
      if not parent:
        raise Exception('UsbDevice.rebuild_from_db(): parent dir not loaded so far!')

      directory = os.path.join(self.mnt_pnt, dirrow[3])

      newdir = DirEntry(root=self, directory=directory, parent=parent, parentid=parentid, dbrebuild=True)
      newdir.dirid[1] = dirid

      parent.dirs.append(newdir)
      dirs[dirid]         = newdir
      self.alldirs[dirid] = newdir

      self.totsubdirs += 1

      # for dirrow in scan dirs


    # rerun all dirs and fill in files

    for dirid, direntry in dirs.iteritems():
      for filerow in self.main.dbhandle.cur.execute("SELECT * FROM Fileentries WHERE usbid=? AND dirid=?;", (self.storid, dirid)):

        # 0=id, 1=dirid, 2=usbid, 3=path, 4=filename, 5=extension, 6=genre, 7=year, 8=title, 9=album, 10=artist

        path = os.path.join(self.mnt_pnt, filerow[3])
        newfile = FileEntry(path, filerow[:3], dbrebuild=True)

        newfile.filename  = filerow[4]
        newfile.extension = filerow[5]
        newfile.GENRE     = filerow[6]
        newfile.YEAR      = filerow[7]
        newfile.TITLE     = filerow[8]
        newfile.ALBUM     = filerow[9]
        newfile.ARTIST    = filerow[10]

        newfile.fix_all_encodings()
        direntry.files.append(newfile)

        self.totfiles += 1

        # for filerow

      # for dirrow in scan files


    self.main.led.set_led_yellow(0)
    self.main.led.set_led_green(0)

    # end rebuild_from_db() #


  def list_all_dirs(self):
    """
    """
    ret = []
    for key, d in self.alldirs.iteritems():
      ret.append("%d %d %s" % (d.dirid[0], d.dirid[1], d.directory))
    return ret

  def list_dirs(self, strdirid):
    """
    """
    if not strdirid: return []

    try:
      dirid = int(strdirid)
    except TypeError:
      return []
    except ValueError:
      return []

    if not dirid in self.alldirs: return []

    ret = []
    for d in self.alldirs[dirid].dirs:
      ret.append("%d %d %s" % (d.dirid[0], d.dirid[1], d.directory))
    return ret

  # end list_dirs() #









