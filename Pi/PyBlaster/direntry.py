"""direntry.py


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import log
import time
import os

from fileentry import FileEntry

class DirEntry:
  """
  """


  def __init__(self, root=None, parent=None, parentid=0, directory=None, dbrebuild=False):
    """
    """

    self.root       = root
    self.parent     = parent
    self.directory  = directory
    self.parentid   = parentid
    self.dirs       = []
    self.files      = []
    self.dirid      = [self.root.storid, self.root.cur_dir_id]

    if not dbrebuild:
      # register dir in main dir list
      self.root.alldirs[self.root.cur_dir_id] = self
      self.root.cur_dir_id += 1
      self.root.totsubdirs += 1
      self.scan_dirs()    # will invoke recursion on subdirs
      self.scan_files()   # will only scan files here


  def scan_dirs(self):
    """
    """
    dirs = sorted([f for f in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, f))])
    for d in dirs:
      subdir = os.path.join(self.directory, d)
      newdir = DirEntry(root=self.root, parent=self, parentid=self.dirid[1], directory=subdir)
      self.dirs.append(newdir)

    # end scan_dirs() #


  def scan_files(self):
    """
    """

    files = sorted([f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f)) and f.endswith(".mp3")])

    file_id = 1

    for f in files:
      mp3 = FileEntry(os.path.join(self.directory, f), [self.dirid[0], self.dirid[1], file_id])
      if mp3.valid:

        # keep led blinking while scanning mp3s
        self.root.main.led.set_led_yellow(file_id % 2)

        self.files.append(mp3)
        file_id += 1

    # turn on led after this dir scaned
    self.root.main.led.set_led_yellow(1)

    self.root.totfiles += len(self.files)

    # end scan_files() #


  def db_insert(self):
    """Insert dir entries into db and after insertion dive into recursion for subdirs

    Intended to have well ordered db scheme
    """

    # insert dirs
    dirs = []
    usbid = self.root.storid
    for d in self.dirs:
      dirname = os.path.relpath(d.directory, self.root.mnt_pnt)
      dirs.append((d.dirid[1], d.parentid, usbid, dirname))
    self.root.main.dbhandle.cur.executemany('INSERT INTO Dirs VALUES (?, ?, ?, ?)', dirs)

    # insert files for this dir
    files = []
    for f in self.files:
      path = os.path.relpath(f.path, self.root.mnt_pnt)
      files.append((f.file_id[2], f.file_id[1], f.file_id[0], path, f.filename, f.extension, f.GENRE, f.YEAR, f.TITLE, f.ALBUM, f.ARTIST, f.length))
    self.root.main.dbhandle.cur.executemany('INSERT INTO Fileentries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', files)

    # insert subdirs
    for d in self.dirs:
      d.db_insert()


    # end db_insert() #



