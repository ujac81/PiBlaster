"""sql.py -- handle to sqlite database

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import sqlite3

import log

DBVERSION = 2


class DBSettings:
    """Enum and create syntax for Usbdevs database table"""
    ID, KEY, VALUE = range(3)

    DropSyntax = """DROP TABLE IF EXISTS Settings;"""
    CreateSyntax = """CREATE TABLE Settings(id INT, key TEXT, value TEXT);"""


class DBHandle:
    """ Manage sqlite db file.
    """
    def __init__(self, main):
        """ Invalidate connector and cursor"""
        self.main = main
        self.con = None
        self.cur = None

    def dbconnect(self):
        """ Load db file, throw if fails

        - Set up connector and cursor
        - Check db version, if too old, rebuild

        Pre: settings object is ready
        Post: DB is ready to use
        """

        try:
            self.con = sqlite3.connect(self.main.settings.dbfile)
            self.cur = self.con.cursor()
        except sqlite3.Error as e:
            self.main.log.write(log.EMERGENCY,
                                "Failed to connect to db file %s: %s" %
                                (self.main.settings.dbfile, e.args[0]))
            raise

        self.main.log.write(log.MESSAGE, "Connected to db file %s" %
                            self.main.settings.dbfile)
        if self.main.settings.rebuilddb:
            self.db_gentables()

        # Check if we got Settings table and if version matches DBVERSION
        # -- rebuild otherwise.

        self.cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE "
                         "type='table' AND name='Settings';")

        if self.cur.fetchone()[0] == 1:
            self.cur.execute("SELECT value FROM Settings WHERE key='version';")
            if self.cur.fetchone()[0] == str(DBVERSION):
                self.main.log.write(log.MESSAGE,
                                    "Found valid version %d in database." %
                                    DBVERSION)
            else:
                self.main.log.write(log.MESSAGE,
                                    "Database is deprecated, rebuilding...")
                self.db_gentables()
        else:
            self.main.log.write(log.MESSAGE,
                                "Database is empty, rebuilding...")
            self.db_gentables()

        self.load_settings()

    def db_gentables(self):
        """Drop all known tables and recreate

        Called if version has changed or -r command line flag found by Settings
        """

        self.cur.executescript(DBSettings.DropSyntax)
        self.con.commit()
        self.cur.executescript(DBSettings.CreateSyntax)
        self.con.commit()

        settings = [(1, "version", "%d" % DBVERSION)]
        self.cur.executemany('INSERT INTO Settings VALUES (?,?,?)', settings)
        self.con.commit()

    def load_settings(self):
        """
        """

        self.main.settings.pin1 = \
            self.get_settings_value("pin1", self.main.settings.pin1_default)
        self.main.settings.pin2 = \
            self.get_settings_value("pin2", self.main.settings.pin2_default)

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
