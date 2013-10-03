"""dbhandle.py manange sqlite db file


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import log
import sqlite3

DBVERSION = 6


class DBHandle:
  """ Manage sqlite db file which contains playlist and known usb devices
  """

  def __init__(self, parent):
    """
    """
    self.parent = parent
    self.con = None
    self.cur = None


    # end __init__() #


  def dbconnect(self):
    """
    """

    try:
      self.con = sqlite3.connect(self.parent.settings.dbfile)
      self.cur = self.con.cursor()
    except sqlite3.Error, e:
      self.parent.log.write(log.EMERGENCY, "Failed to connect to db file %s: %s" % (self.parent.settings.dbfile, e.args[0]))
      raise

    self.parent.log.write(log.MESSAGE, "Connected to db file %s" % self.parent.settings.dbfile)
    if self.parent.settings.rebuilddb: self.db_gentables()

    # check if we got Settings table and if version matches DBVERSION -- rebuild otherwise

    self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    if 'Settings' in self.cur.fetchone():
      self.cur.execute("SELECT value FROM Settings WHERE key='version';")
      if self.cur.fetchone()[0] == str(DBVERSION):
        self.parent.log.write(log.MESSAGE, "Found valid version %d in database." % DBVERSION)
      else:
        self.parent.log.write(log.MESSAGE, "Database is deprecated, rebuilding...")
        self.db_gentables()
    else:
      self.parent.log.write(log.MESSAGE, "Database is empty, rebuilding...")
      self.db_gentables()

    # remove broken and orphaned entries (if shut down while creating rows)
    self.cleandb()


    # end dbconnect() #


  def db_gentables(self):
    """
    """

    self.cur.executescript("""DROP TABLE IF EXISTS Settings;
       DROP TABLE IF EXISTS Usbdevs;
       DROP TABLE IF EXISTS Dirs;
       DROP TABLE IF EXISTS Fileentries;
       CREATE TABLE Settings(id INT, key TEXT, value TEXT);
       CREATE TABLE Usbdevs(id INT, UUID TEXT, md5 TEXT, scanok INT);
       CREATE TABLE Dirs(id INT, parentid INT, usbid INT, dirname TEXT);
       CREATE TABLE Fileentries(id INT, dirid INT, usbid INT, path TEXT, filename TEXT, extension TEXT, genre TEXT, year INT, title TEXT, album TEXT, artist TEXT);""")
    self.con.commit()

    settings = [(1, "version", "%d" % DBVERSION)]
    self.cur.executemany('INSERT INTO Settings VALUES (?,?,?)', settings)
    self.con.commit()


  def cleandb(self):
    """
    """

    # TODO: Scan for non-ok usbdevs and for dir/file entries without valid usbdev and remove them



  def get_usbid(self, UUID):
    """ get latest usb stick id for usb mananger while creating new UsbDevive entries

    We know that all usb entries are at OK state 1 here as cleandb() has been run on startup
    """
    lastid = -1
    for row in self.cur.execute("SELECT id, UUID FROM Usbdevs ORDER BY id;"):
      if row[1] == UUID: return row[0]
      lastid = row[0]

    return lastid + 1

    # end get_usbid() #


  def check_usb_md5(self, UUID, md5):
    """ Check if md5 for dir structure matches md5 for stick with UUID in database
    """
    for row in self.cur.execute("SELECT UUID, md5 FROM Usbdevs;"):
      if row[0] == UUID and row[1] == md5: return True

    return False

    # end check_usb_md5() #


  def drop_changed_usbdev(self, usbdevid):
    """Drop dir/file entries for usb device

    Called by usbdevice if md5 changed and by cleandb if scanok=0
    """

    self.parent.log.write(log.MESSAGE, "Dropping outdated or incomplete dir/file data for usb device #%d" % usbdevid)

    # end drop_changed_usbdev() #


  def add_or_update_usb_stor(self, usbdevid, UUID, md5):
    """ Check if we have usbdev for UUID, if then update md5, insert into db otherwise
    """

    for row in self.cur.execute("SELECT UUID, md5 FROM Usbdevs;"):
      if row[0] == UUID:
        if row[1] == md5:
          # we found valid db entries, nothing to do
          return True # ==> no rescan rebuild dirs/files from db
        else:
          # md5 became invalid (content changed) ==> drop dir/file entries, register new md5 and set scanok to 0
          self.parent.log.write(log.MESSAGE, "Updating usb device %s with id %d to new md5 %s" % (UUID, usbdevid, md5))
          self.drop_changed_usbdev(usbdevid)
          self.cur.execute("UPDATE Usbdevs SET md5=?, scanok=0 WHERE id=?", (md5, usbdevid))
          self.con.commit()
          return False # ==> rescan

    # No return so far -> new entry
    self.parent.log.write(log.MESSAGE, "Registering usb device %s with id %d and known md5 %s" % (UUID, usbdevid, md5))
    self.cur.execute('INSERT INTO Usbdevs (id, UUID, md5, scanok) VALUES (?, ?, ?, ?)', (usbdevid, UUID, md5, 0,))
    self.con.commit()
    return False # ==> scan device

    # end add_or_update_usb_stor() #


  def set_scan_ok(self, usbdevid):
    """ Set scanok flag to 1 after scan has finished
    """
    self.cur.execute("UPDATE Usbdevs SET scanok=1 WHERE id=?", (usbdevid,))
    self.con.commit()

