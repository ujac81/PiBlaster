"""playlistmanager.py -- Manage multiple playlists

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from playlist import PlayList


class PlayListManager:

  def __init__(self, parent):
    """Set up empty playlist hash and None active playlist"""

    self.parent = parent
    self.playlists = {}     # id: PlayList
    self.activeplaylist = None

    # end __init__() #

  def load_playlists(self):
    """Create playlist objects from databse"""

    # TODO only load default (0) playlist, rest will live from databse

    #for row in self.parent.dbhandle.cur.execute(
        #"SELECT * FROM Playlists ORDER BY id;"):
      #newlist = PlayList(self, row)
      #self.playlists[newlist.index] = newlist
      #if newlist.index == 0:
        #self.activeplaylist = self.playlists[newlist.index]

    # end load_playlists() #
