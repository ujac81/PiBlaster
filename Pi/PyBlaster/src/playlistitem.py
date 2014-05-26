"""playitem.py -- single entry in PlayList

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from dbhandle import DBFileEntries as FE


class PlayListItem:

    def __init__(self, db_row, is_connected, revision):
        """
        """
        self.db_row = db_row
        self.is_connected = is_connected
        self.revision = revision
        self.played = 0

        # end __init__() #

    def print_self(self, printformat="||$disptitle$||$length$||"):
        """
        """

        # USB device is not connected now
        if not self.is_connected:
            return None

        res = printformat

        res = res.replace("$artist$", self.db_row[FE.ARTIST])
        res = res.replace("$disptitle$", self.db_row[FE.DISPTITLE])
        res = res.replace("$length$", "%d" % self.db_row[FE.TIME])
        res = res.replace("$title$", self.db_row[FE.TITLE])

        return res

    def append_to_db_list(self, listref, listid, entryid, state):
        """
        """

        listref.append([listid, entryid, self.db_row[FE.STORID],
                        self.revision, self.db_row[FE.DIRID],
                        self.db_row[FE.ID], self.db_row[FE.DISPTITLE],
                        self.played, self.db_row[FE.PATH], state
                        ])

    def set_connected_by_storid(self, storid, is_connected):
        """
        """
        if self.db_row[FE.STORID] == storid:
            self.is_connected = is_connected
            return 1
        return 0

    def check_revision_matches(self, revision, usbdev):
        """Called on USB-connect to check if file ids may have changed

        If revision is unchanged, all file ids are still valid.
        If revision has changed get new ids tripple by path,
        If None, return False which will prevent reinsertion into playlist.
        """
        if revision == self.revision:
            return True

        self.revision = revision

        newrow = usbdev.get_fileentry_by_path(self.db_row[FE.PATH])
        if newrow is None:
            return False

        self.db_row = newrow

        return True
