"""playlistmanager.py -- Manage active playlist

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""


import log
from playlistitem import PlayListItem




class PlayListManager:

  def __init__(self, parent):
    """Set up empty playlist hash and None active playlist"""

    self.parent         = parent

    self.playlist       = []
    self.playlist_pos   = 0
    self.playlist_id    = 0       # id of the source playlist in database
                                  # 0 = new playlist

    # end __init__() #

  def load_playlist(self):
    """Load last playlist from database"""

    # TODO load.

    # end load_playlist() #

  def save(self):
    """Write playlist to source playlist in database

    Uses self.playlist_id to identify correct playlist in db.
    Won't work if self.playlist_id == 0 (new playlist)

    Returns True if success, False if id == 0 or failed to write.
    """

    if self.playlist_id == 0:
      return False

    ### TODO save to db

    return True

    # end save() #

  def save_as(self, name):
    """Write new playlist to database

    Returns True if success, False if name exists or failed to write.
    """

    ### TODO save as

    return True

    # end save_as() #

  def clear(self):
    """Clean out active playlist (0) and set id to 0"""

    self.playlist = []
    self.playlist_pos = 0
    self.playlist_id = 0

    self.parent.log.write(log.MESSAGE, "[PLAYLISTMNGR] cleared.")

    # end clear() #


  def insert_item(self, ids, position=-1,
                  random_insert=False, after_current=False):
    """Push back item from database to playlist.

    Keywords:
      ids           -- [usbstorid, dirid, fileid] from database]
      position      -- insert position in playlist if not random
                       and not after_current
      random_insert -- put somewhere in playlist
      after_current -- insert after current track

    Returns: True if insert ok.
    """

  def insert_dir(self, ids, position=-1,
                 random_insert=False, after_current=False):
    """Push back alld die items from database to playlist.

    Keywords:
      ids           -- [usbstorid, dirid, fileid] from database]
      position      -- insert position in playlist if not random
                       and not after_current (-1 = append)
      random_insert -- put somewhere in playlist
      after_current -- insert after current track

    Returns: Number of insertions
    """

    ins_cnt = 0

    is_connected = self.parent.usb.is_connected(ids[0])
    revision     = self.parent.usb.revision(ids[0])

    for row in self.parent.dbhandle.cur.execute(
        "SELECT * FROM Fileentries WHERE dirid=? AND usbid=? ORDER BY id",
        (ids[1], ids[0],)):
      self.playlist.append(PlayListItem(row, is_connected, revision))
      ins_cnt += 1

    return ins_cnt

  def list_playlist(self,
                    playlist=0,
                    printformat="||$artist$||$title$||$length$||",
                    max_items=1000, start_at=0):
    """Show current playlist

    Keywords:
      playlist    -- print playlist #id (0 = current playlist)
      printformat -- see PlayListItem.print_item() for format info
      max_items   -- do not show more than N items
      start_at    -- start displaying at position N

    Returns string list: [Position, item count, item0, item1, ... itemN-1]
    """

    res = [0, 0]

    if playlist == 0:
      res = [self.playlist_pos, 0]

      for i in range(start_at, min(len(self.playlist), max_items)):
        res.append(self.playlist[i].print_item(printformat))

    else:
      """do something """
      ### TODO: build result from database


    res[1] = len(res) - 2

    return res










