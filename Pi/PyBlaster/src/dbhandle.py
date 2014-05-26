"""dbhandle.py -- Manange sqlite db file



@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import sqlite3

import log

DBVERSION = 20


class DBDirEntries:
    """Enum and create syntax for Dirs database table

    Directory is uniquely identified by [id, usbid] key pair.
    Key pair may change if changes on drive detected.
    'path' may be used to reassign ids to prevent full rescan if directories
    where copied by FileManager.
    Initial assignment by UsbDevive.recursive_rescan_into_db().

    id      -- directory id (NOT primary key!)
    parentid-- id of parent directory
    usbid   -- usb device id (id in Usbdevs table)
    numdirs -- number of subdirs in this dir
    numfiles-- number of files in this dir
    dirname -- directory name
    path    -- rel path on drive (redundant, but good for fast id reassignment)

    """

    ID, PARENTID, USBID, NUMDIRS, NUMFILES, DIRNAME, PATH = range(7)

    DropSyntax = """DROP TABLE IF EXISTS Dirs;"""
    CreateSyntax = """CREATE TABLE Dirs(
        id INT, parentid INT, usbid INT, numdirs INT,
        numfiles INT, dirname TEXT, path TEXT);"""

    # end class DBDirEntries #


class DBFileEntries:
    """Enum and create syntax for Fileentries database table

    File is uniquely identified by [id, dirid, usbid] key pair.
    'id' is NO PRIMARY KEY.
    Initial assignment by UsbDevive.recursive_rescan_into_db().
    Directory id may be changed if directory structure was changed by
    FileManager.

    id          -- id of file in current directory (NOT primary key!)
    dirid       -- directory id in Dirs table
    usbid       -- usb device id in Usbdevs table
    path        -- rel path on drive
    filename    -- last part of path
    extension   -- like 'mp3' or 'ogg'
    genre       -- ID3 genre tag or 'Unknown Genre'
    year        -- ID3 year tag or 0
    title       -- ID3 title tag or filename
    album       -- ID3 album tag or 'Unknown Album'
    artist      -- ID3 artist tag or 'Unknown Artist'
    time        -- time data in seconds from mutagen
    disptitle   -- "artist - title" if found or filename
    """
    ID, DIRID, STORID, PATH, FILENAME, EXT, GENRE, YEAR, TITLE, ALBUM, \
    ARTIST, TIME, DISPTITLE = range(13)

    DropSyntax = """DROP TABLE IF EXISTS Fileentries;"""
    CreateSyntax = """CREATE TABLE Fileentries(
        id INT, dirid INT, usbid INT, path TEXT,
        filename TEXT, extension TEXT, genre TEXT,
        year INT, title TEXT, album TEXT,
        artist TEXT, time INT, disptitle TEXT);"""

    # end class DBFileEntries #


class DBPlayLists:
    """Enum and create syntax for Usbdevs database table"""
    ID, NAME, CREATED, CREATOR, POSITION, STATE = range(6)

    # id         -- playlist id
    # name       -- given name for this list, should be unique
    # created    -- creation date
    # creator    -- creator name
    # position   -- current track position = index in Playlists
    # state      -- state index, increased with every playlist change
    #               required for undo actions

    DropSyntax = """DROP TABLE IF EXISTS Playlists;"""
    CreateSyntax = """CREATE TABLE Playlists(
        id INT, name TEXT, created INT, creator TEXT,
        position INT, state INT);"""

    # end class DBPlayLists #


class DBPlayListEntries:
    """Enum and create syntax for Usbdevs database table"""
    ID, INDEX, STORID, REVISION, DIRID, FILEID, TITLE, PLAYED, PATH, \
    STATE = range(10)

    # playlistid -- refers to id in Playlists
    # position   -- position in playlist
    # usbid      -- usb device id of track
    # usbrev     -- usb revision number in moment of add
    # dirid      -- directory id on device
    # fileid     -- file id in directory
    # disptitle  -- display text in playlist
    # played     -- = 1 if item played (for random walk)
    # path       -- path on device (if revision change, but path stil valid)
    # state      -- state index of add action (for undo add)

    DropSyntax = """DROP TABLE IF EXISTS Playlistentries;"""
    CreateSyntax = """CREATE TABLE Playlistentries(
        playlistid INT, position INT,
        usbid INT, usbrev INT, dirid INT,
        fileid INT, disptitle TEXT, played INT, path TEXT, state INT);"""

    # end class DBPlayListEntries #


class DBUsbDevs:
    """Enum and create syntax for Usbdevs database table"""
    ID, UUID, MD5, SCANOK, ALIAS, REVISION = range(6)

    DropSyntax = """DROP TABLE IF EXISTS Usbdevs;"""
    CreateSyntax = """CREATE TABLE Usbdevs(
        id INT, UUID TEXT, md5 TEXT, scanok INT,
        alias TEXT, revision INT, bytesfree INT, bytesused INT);"""

    # end class DBUsbDevs #


class DBSettings:
    """Enum and create syntax for Usbdevs database table"""
    ID, KEY, VALUE = range(3)

    DropSyntax = """DROP TABLE IF EXISTS Settings;"""
    CreateSyntax = """CREATE TABLE Settings(id INT, key TEXT, value TEXT);"""

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
        Post: DB is ready to use
        """

        try:
            self.con = sqlite3.connect(self.parent.settings.dbfile)
            self.cur = self.con.cursor()
        except sqlite3.Error as e:
            self.parent.log.write(log.EMERGENCY,
                                  "Failed to connect to db file %s: %s" %
                                  (self.parent.settings.dbfile, e.args[0]))
            raise

        self.parent.log.write(log.MESSAGE, "Connected to db file %s" %
                              self.parent.settings.dbfile)
        if self.parent.settings.rebuilddb:
            self.db_gentables()

        # Check if we got Settings table and if version matches DBVERSION
        # -- rebuild otherwise.

        self.cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE "
                         "type='table' AND name='Settings';")

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
            self.parent.log.write(log.MESSAGE,
                                  "Database is empty, rebuilding...")
            self.db_gentables()

        self.load_settings()

        # Remove broken and orphaned entries (if shut down while creating rows)
        self.cleandb()

        # end dbconnect() #

    def db_gentables(self):
        """Drop all known tables and recreate

        Called if version has changed or -r command line flag found by Settings
        """

        self.cur.executescript(DBDirEntries.DropSyntax +
                               DBFileEntries.DropSyntax +
                               DBPlayLists.DropSyntax +
                               DBPlayListEntries.DropSyntax +
                               DBUsbDevs.DropSyntax +
                               DBSettings.DropSyntax)
        self.con.commit()
        self.cur.executescript(DBDirEntries.CreateSyntax +
                               DBFileEntries.CreateSyntax +
                               DBPlayLists.CreateSyntax +
                               DBPlayListEntries.CreateSyntax +
                               DBUsbDevs.CreateSyntax +
                               DBSettings.CreateSyntax)
        self.con.commit()

        settings = [(1, "version", "%d" % DBVERSION)]
        self.cur.executemany('INSERT INTO Settings VALUES (?,?,?)', settings)
        self.con.commit()

    def cleandb(self):
        """Remove data for usbdevices if scanning did not finish successfully

        Called on dbconnect().
        """

        # Collect all storage ids which did not finish their scan.
        remove_stors = []
        for row in self.cur.execute("SELECT id FROM Usbdevs WHERE scanok=0;"):
            remove_stors.append(row[0])

        # Drop all entries for failed scans.
        for storid in remove_stors:
            self.parent.log.write(log.MESSAGE, "Removing broken entries for "
                                               "storage %d from database..."
                                               % storid)
            self.cur.execute('DELETE FROM Fileentries WHERE usbid=?',
                             (storid, ))
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
        # else:
            # drop all entries that have no valid storage id
            # valid_list = ','.join(valid_stors)

            # TODO    this somehow does not work --
            # should remove entries without valid storage id,
            # but kills too much...

            #self.cur.execute(
            # 'DELETE FROM Fileentries WHERE usbid NOT IN (?)', (valid_list, ))
            #self.cur.execute(
            # 'DELETE FROM Dirs WHERE usbid NOT IN (?)', (valid_list, ))
            #self.con.commit()

        # end cleandb() #

    def get_usbid(self, uuid):
        """Get usb id for usb mananger while creating new UsbDevive entries

        If unkown, largest id + 1 is returned.    We know that all usb entries
        are at OK state 1 here as cleandb() has been run on startup.

        return [storid, alias, revision]
        """
        lastid = -1
        for row in self.cur.execute("SELECT id, UUID, alias, revision FROM "
                                    "Usbdevs ORDER BY id;"):
            if row[1] == uuid:
                return [row[0], row[2], row[3]]
            lastid = row[0]

        return [lastid + 1, None, 0]

        # end get_usbid() #

    def check_usb_md5(self, uuid, md5):
        """Check if md5 for matches md5 for stick with UUID in database."""

        for row in self.cur.execute("SELECT UUID, md5 FROM Usbdevs;"):
            if row[0] == uuid and row[1] == md5:
                return True

        return False

        # end check_usb_md5() #

    def drop_changed_usbdev(self, usbdevid):
        """Drop dir/file entries for usb device

        Called by usbdevice if md5 changed and by cleandb if scanok=0.
        """

        self.parent.log.write(log.MESSAGE, "Dropping outdated or incomplete "
                                           "dir/file data for usb device "
                                           "#%d" % usbdevid)

        self.cur.execute('DELETE FROM Fileentries WHERE usbid=?', (usbdevid, ))
        self.cur.execute('DELETE FROM Dirs WHERE usbid=?', (usbdevid, ))
        self.con.commit()

        # end drop_changed_usbdev() #

    def add_or_update_usb_stor(self, usbdevid, uuid, md5):
        """ Check if we have usbdev for UUID.

        If found update md5, otherwise insert into db.
        """

        for row in self.cur.execute("SELECT UUID, md5, scanok FROM Usbdevs"):
            if row[0] == uuid:
                if row[1] == md5 and row[2] == 1:
                    # we found valid db entries, nothing to do
                    return True  # ==> no rescan rebuild dirs/files from db
                else:
                    # md5 became invalid (content changed)
                    # ==> drop dir/file entries,
                    #     register new md5 and set scanok to 0
                    self.parent.log.write(log.MESSAGE, "Updating usb device "
                                                       "%s with id %d to new "
                                                       "md5 %s" % (uuid,
                                                                   usbdevid,
                                                                   md5))
                    self.drop_changed_usbdev(usbdevid)
                    self.cur.execute("UPDATE Usbdevs SET md5=?, scanok=0 "
                                     "WHERE id=?", (md5, usbdevid))
                    self.con.commit()
                    return False  # ==> rescan

        # No return so far -> new entry
        self.parent.log.write(log.MESSAGE, "Registering usb device %s with "
                                           "id %d and known md5 %s" %
                                           (uuid, usbdevid, md5))
        self.cur.execute('INSERT INTO Usbdevs (id, UUID, md5, scanok, alias, '
                         'revision, bytesfree, bytesused ) VALUES (?, ?, ?, '
                         '?, ?, ?, ?, ?)', (usbdevid, uuid, md5, 0, uuid, 0,
                                            0, 0))
        self.con.commit()
        return False  # ==> scan device

        # end add_or_update_usb_stor() #

    def set_scan_ok(self, usbdevid, revision, free, used):
        """Set scanok flag to 1 after scan has finished"""

        self.cur.execute("UPDATE Usbdevs SET scanok=1, revision=?, "
                         "bytesfree=?, bytesused=? WHERE id=?",
                         (revision, free, used, usbdevid))
        self.con.commit()

    def invalidate_md5(self, usbdevid):
        """ Destroy md5 hash for device to enforce rescanning"""

        self.cur.execute("UPDATE Usbdevs SET md5=? WHERE id=?",
                         ("xxx", usbdevid,))
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

    def load_settings(self):
        """
        """

        self.parent.settings.pin1 = \
            self.get_settings_value("pin1", self.parent.settings.pin1_default)
        self.parent.settings.pin2 = \
            self.get_settings_value("pin2", self.parent.settings.pin2_default)

        # end load_settings() #

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

        self.cur.execute('INSERT INTO Settings (id, key, value)'
                         ' VALUES (?, ?, ?)', (new_id, key, value))
        self.con.commit()

        # end set_settings_value() #

    def get_settings_value(self, key, fallback=None):
        """
        """

        res = fallback
        for row in self.cur.execute("SELECT value FROM Settings WHERE key=?",
                                    (key,)):
            res = row[0]
        return res

    def get_settings_value_as_int(self, key, fallback=-1):
        """
        """
        strres = self.get_settings_value(key)
        if strres is None:
            return fallback

        try:
            res = int(strres)
        except TypeError:
            res = fallback
        except ValueError:
            res = fallback

        return res

        # end get_settings_value_as_int #

    # end class DBHandle #
