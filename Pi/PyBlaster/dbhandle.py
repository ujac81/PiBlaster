"""dbhandle.py -- Manange sqlite db file


Database structure::

Settings(id INT, key TEXT, value TEXT)::
  holds (key, value) pairs with settings that may be changed during
  runtime (not persistant from config file)

  Items in Settings::

    version = DBVERSION  -- version of table layout, rebuild if outdated


Usbdevs(id INT, UUID TEXT, md5 TEXT, scanok INT,
        alias TEXT, revision INT)::

  Handled by UsbDevive

  Holds data about known usb devices. If an id is assigned once to
  a device, this id should be persistant.

  id        -- storage id, unique via UUID
  UUID      -- almost unique UUID from blkid, required to
               identify device
  md5       -- digest of file tree, if outdated -> rescan and increase
               revision
  scanok    -- set to 1 after successful scan, if not 1 -> rescan
  alias     -- name assigned for this device
  revision  -- incremented if md5 changed -> invalidate playlist entries
               for this device

Dirs(id INT, parentid INT, usbid INT, numdirs INT,
     numfiles INT, dirname TEXT)

  Reflects a directory node identifid by [storage_id, dir_id].

  0 id        -- incremental directory id on this storage
  1 parentid  -- parent directory id
  2 usbid     -- storage id (UsbDevive)
  3 numdirs   -- number of subdirs
  4 numfiles  -- number of mp3s in dir
  5 dirname   -- name (not path) of this directory


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import sqlite3

import log

DBVERSION = 14


class DBDirEntries:
  """Enum and create syntax for Dirs database table"""

  ID, PARENTID, USBID, NUMDIRS, NUMFILES, DIRNAME = range(6)

  DropSyntax    = """DROP TABLE IF EXISTS Dirs;"""
  CreateSyntax  = """CREATE TABLE Dirs(
    id INT, parentid INT, usbid INT, numdirs INT,
    numfiles INT, dirname TEXT);"""

  # end class DBDirEntries #


class DBFileEntries:
  """Enum and create syntax for Fileentries database table"""
  ID, DIRID, STORID, PATH, FILENAME, EXT, GENRE, YEAR, TITLE, \
  ALBUM, ARTIST, TIME, DISPTITLE = range(12)

  DropSyntax    = """DROP TABLE IF EXISTS Fileentries;"""
  CreateSyntax  = """CREATE TABLE Fileentries(
    id INT, dirid INT, usbid INT, path TEXT,
    filename TEXT, extension TEXT, genre TEXT,
    year INT, title TEXT, album TEXT,
    artist TEXT, time INT, disptitle TEXT);"""

  # end class DBFileEntries #


class DBPlayLists:
  """Enum and create syntax for Usbdevs database table"""
  ID, NAME, CREATED, CREATOR, ITEMSCOUNT, POSITION = range(6)

  DropSyntax    = """DROP TABLE IF EXISTS Playlists;"""
  CreateSyntax  = """CREATE TABLE Playlists(
    id INT, name TEXT, created INT, creator TEXT,
    itemcount INT, position INT);"""

  # end class DBPlayLists #


class DBPlayListEntries:
  """Enum and create syntax for Usbdevs database table"""
  ID, INDEX, STORID, REVISION, DIRID, FILEID, TITLE, PLAYED = range(8)

  DropSyntax    = """DROP TABLE IF EXISTS Playlistentries;"""
  CreateSyntax  = """CREATE TABLE Playlistentries(
    playlistid INT, entryin INT,
    usbid INT, usbrev INT, dirid INT,
    fileid INT, disptitle TEXT, played INT);"""

  # end class DBPlayListEntries #

class DBUsbDevs:
  """Enum and create syntax for Usbdevs database table"""
  ID, UUID, MD5, SCANOK, ALIAS, REVISION = range(6)

  DropSyntax    = """DROP TABLE IF EXISTS Usbdevs;"""
  CreateSyntax  = """CREATE TABLE Usbdevs(
    id INT, UUID TEXT, md5 TEXT, scanok INT,
    alias TEXT, revision INT);"""

  # end class DBUsbDevs #


class DBSettings:
  """Enum and create syntax for Usbdevs database table"""
  ID, KEY, VALUE = range(3)

  DropSyntax    = """DROP TABLE IF EXISTS Settings;"""
  CreateSyntax  = """CREATE TABLE Settings(
    id INT, key TEXT, value TEXT);"""

  # end class DBUsbDevs #



class DBHandle:
  """ Manage sqlite db file which contains playlist and known usb devices

  Provides:
    - list of known USB devices by device id
    - new device internal device id assignment
    - search routines
    - playlist routines
  """
  def __init__(self, parent):
    """ Invalidate connector and cursor"""
    self.parent = parent
    self.con = None
    self.cur = None

    # end __init__() #

  def dbconnect(self):
    """ Load db file, throw if fails

    - Set up connector and cursor
    - Check db version, if too old, rebuild
    - Clean up orphaned entries from db

    Pre: settings object is ready
    Post: DB is ready for usage
    """

    try:
      self.con = sqlite3.connect(self.parent.settings.dbfile)
      self.cur = self.con.cursor()
    except sqlite3.Error, e:
      self.parent.log.write(log.EMERGENCY,
                            "Failed to connect to db file %s: %s" %
                            (self.parent.settings.dbfile, e.args[0]))
      raise

    self.parent.log.write(log.MESSAGE, "Connected to db file %s" %
                          self.parent.settings.dbfile)
    if self.parent.settings.rebuilddb: self.db_gentables()

    # Check if we got Settings table and if version matches DBVERSION
    # -- rebuild otherwise.

    self.cur.execute("SELECT COUNT(name) FROM sqlite_master "\
      "WHERE type='table' AND name='Settings';")

    if self.cur.fetchone()[0] == 1:
      self.cur.execute("SELECT value FROM Settings WHERE key='version';")
      if self.cur.fetchone()[0] == str(DBVERSION):
        self.parent.log.write(log.MESSAGE,
                              "Found valid version %d in database." %
                              DBVERSION)
      else:
        self.parent.log.write(log.MESSAGE,
                              "Database is deprecated, rebuilding...")
        self.db_gentables()
    else:
      self.parent.log.write(log.MESSAGE, "Database is empty, rebuilding...")
      self.db_gentables()

    # Remove broken and orphaned entries (if shut down while creating rows).
    self.cleandb()

    # end dbconnect() #

  def db_gentables(self):
    """Drop all known tables and recreate

    Called if version has changed or -r command line flag found by Settings.
    """

    self.cur.executescript(DBDirEntries.DropSyntax+
                           DBFileEntries.DropSyntax+
                           DBPlayLists.DropSyntax+
                           DBPlayListEntries.DropSyntax+
                           DBUsbDevs.DropSyntax+
                           DBSettings.DropSyntax)
    self.con.commit()
    self.cur.executescript(DBDirEntries.CreateSyntax+
                           DBFileEntries.CreateSyntax+
                           DBPlayLists.CreateSyntax+
                           DBPlayListEntries.CreateSyntax+
                           DBUsbDevs.CreateSyntax+
                           DBSettings.CreateSyntax)
    self.con.commit()

    settings = [(1, "version", "%d" % DBVERSION)]
    self.cur.executemany('INSERT INTO Settings VALUES (?,?,?)', settings)
    self.con.commit()

  def cleandb(self):
    """Remove data for usbdevices where scanning did not finish successfully

    Called on dbconnect().
    """

    # Collect all storage ids which did not finish their scan.
    remove_stors = []
    for row in self.cur.execute("SELECT id FROM Usbdevs WHERE scanok=0;"):
      remove_stors.append(row[0])

    # Drop all entries for failed scans.
    for storid in remove_stors:
      self.parent.log.write(log.MESSAGE,
        "Removing broken entries for storage %d from database..." % storid)
      self.cur.execute('DELETE FROM Fileentries WHERE usbid=?', (storid, ))
      self.cur.execute('DELETE FROM Dirs WHERE usbid=?', (storid, ))
      self.con.commit()

    # Generate list of valid storage ids.
    valid_stors = []
    for row in self.cur.execute("SELECT id FROM Usbdevs WHERE scanok=1;"):
      valid_stors.append(str(row[0]))

    if not valid_stors:
      # if no valid_stors, drop all
      self.cur.execute('DELETE FROM Fileentries')
      self.cur.execute('DELETE FROM Dirs')
      self.con.commit()
    else:
      # drop all entries that have no valid storage id
      valid_list = ','.join(valid_stors)

      # TODO  this somehow does not work --
      # should remove entries without valid storage id, but kills too much...

      #self.cur.execute(
      # 'DELETE FROM Fileentries WHERE usbid NOT IN (?)', (valid_list, ))
      #self.cur.execute(
      # 'DELETE FROM Dirs WHERE usbid NOT IN (?)', (valid_list, ))
      #self.con.commit()

    # end cleandb() #

  def get_usbid(self, UUID):
    """Get usb stick id for usb mananger while creating new UsbDevive entries"

    Ff unkown, largest id + 1 is returned.  We know that all usb entries
    are at OK state 1 here as cleandb() has been run on startup.

    return [storid, alias, revision]
    """
    lastid = -1
    for row in self.cur.execute(
        "SELECT id, UUID, alias, revision FROM Usbdevs ORDER BY id;"):
      if row[1] == UUID:
        return [row[0], row[2], row[3]]
      lastid = row[0]

    return [lastid + 1, None, 0]

    # end get_usbid() #


  def check_usb_md5(self, UUID, md5):
    """Check if md5 for matches md5 for stick with UUID in database."""

    for row in self.cur.execute("SELECT UUID, md5 FROM Usbdevs;"):
      if row[0] == UUID and row[1] == md5:
        return True

    return False

    # end check_usb_md5() #

  def drop_changed_usbdev(self, usbdevid):
    """Drop dir/file entries for usb device

    Called by usbdevice if md5 changed and by cleandb if scanok=0.
    """

    self.parent.log.write(log.MESSAGE,
      "Dropping outdated or incomplete dir/file data for usb device #%d" %
      usbdevid)

    self.cur.execute('DELETE FROM Fileentries WHERE usbid=?', (usbdevid, ))
    self.cur.execute('DELETE FROM Dirs WHERE usbid=?', (usbdevid, ))
    self.con.commit()

    # end drop_changed_usbdev() #


  def add_or_update_usb_stor(self, usbdevid, UUID, md5):
    """ Check if we have usbdev for UUID.

    Ff then update md5, insert into db otherwise.
    """

    for row in self.cur.execute("SELECT UUID, md5, scanok FROM Usbdevs"):
      if row[0] == UUID:
        if row[1] == md5 and row[2] == 1:
          # we found valid db entries, nothing to do
          return True # ==> no rescan rebuild dirs/files from db
        else:
          # md5 became invalid (content changed)
          # ==> drop dir/file entries, register new md5 and set scanok to 0
          self.parent.log.write(log.MESSAGE,
            "Updating usb device %s with id %d to new md5 %s" %
            (UUID, usbdevid, md5))
          self.drop_changed_usbdev(usbdevid)
          self.cur.execute(
            "UPDATE Usbdevs SET md5=?, scanok=0 WHERE id=?", (md5, usbdevid))
          self.con.commit()
          return False # ==> rescan

    # No return so far -> new entry
    self.parent.log.write(log.MESSAGE,
      "Registering usb device %s with id %d and known md5 %s" %
      (UUID, usbdevid, md5))
    self.cur.execute(
      'INSERT INTO Usbdevs (id, UUID, md5, scanok, alias, revision) ' \
      'VALUES (?, ?, ?, ?, ?, ?)', (usbdevid, UUID, md5, 0, UUID, 0 ))
    self.con.commit()
    return False # ==> scan device

    # end add_or_update_usb_stor() #

  def set_scan_ok(self, usbdevid, revision):
    """Set scanok flag to 1 after scan has finished"""

    self.cur.execute("UPDATE Usbdevs SET scanok=1, revision=? WHERE id=?",
                     (revision, usbdevid,))
    self.con.commit()

  def invalidate_md5(self, usbdevid):
    """ Destroy md5 hash for device to enforce rescanning"""

    self.cur.execute("UPDATE Usbdevs SET md5=? WHERE id=?", ("xxx", usbdevid,))
    self.con.commit()

  def update_alias(self, usbdevid, alias):
    """Change alias in database for usb device

    return False if alias exists in database.
    """

    for row in self.cur.execute("SELECT alias FROM Usbdevs"):
      if row[0] == alias:
        return False

    self.cur.execute("UPDATE Usbdevs SET alias=? WHERE id=?",
                     (alias, usbdevid,))
    self.con.commit()
    return True


  def set_settings_value(self, key, value):
    """
    """

    # delete current settings val from database
    self.cur.execute("DELETE FROM Settings WHERE key=?", (key,))
    self.con.commit()

    # get id for new object
    new_id = 0
    for row in self.cur.execute("SELECT id FROM Settings ORDER BY id"):
      new_id = row[0]
    new_id += 1

    self.cur.execute( 'INSERT INTO Settings (id, key, value) VALUES (?, ?, ?)',
      (new_id, key, value))
    self.con.commit()

    # end set_settings_value() #


  def get_settings_value(self, key):
    """
    """

    res = None
    for row in self.cur.execute(
        "SELECT value FROM Settings WHERE key=?", (key,)):
      res = row[0]
    return res


  def get_settings_value_as_int(self, key):
    """
    """
    res = -1
    strres = get_settings_value(key)
    if strres is None:
      return -1

    try:
      res = int(strres)
    except TypeError:
      res = -1
    except ValueError:
      res = -1

    return res



