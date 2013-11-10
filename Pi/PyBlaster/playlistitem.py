"""playitem.py -- single entry in PlayList

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from dbhandle import DBFileEntries as FE


class PlayListItem:

  def __init__(self, db_row, is_connected, revision):
    """
    """
    self.db_row       = db_row        # row from databse
    self.is_connected = is_connected  #
    self.revision     = revision
    self.disptitle    = u'%s - %s' % ( db_row[FE.ARTIST], db_row[FE.TITLE] )
    self.played       = 0

    if db_row[FE.ARTIST] == u'Unknown Artist':
      self.disptitle = db_row[FE.TITLE]


    # end __init__() #


  def print_item(self, printformat="||$disptitle$||$length$||"):
    """
    """
    res = printformat

    res = res.replace("$artist$", self.db_row[FE.ARTIST])
    res = res.replace("$disptitle$", self.disptitle)
    res = res.replace("$length$", "%d" % self.db_row[FE.TIME])
    res = res.replace("$title$", self.db_row[FE.TITLE])


    return res

    # end print_item() #

  def append_to_db_list(self, listref, listid, entryid):
    """
    """

    listref.append([listid, entryid, self.db_row[FE.STORID],
                    self.revision, self.db_row[FE.DIRID],
                    self.db_row[FE.ID], self.disptitle,
                    self.played])


