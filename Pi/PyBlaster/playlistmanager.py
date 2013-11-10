"""playlistmanager.py -- Manage active playlist

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import time

import log
from dbhandle import DBPlayLists as PL
from dbhandle import DBPlayListEntries as PE
from playlistitem import PlayListItem


class PlayListManager:

  def __init__(self, parent):
    """Empty ctor

    Need to call load_playlist after other object initialized.
    """

    self.parent = parent

    # end __init__() #

  def clear(self):
    """Clean out active playlist (0) and set id to 0"""

    self.playlist       = []
    self.playlist_pos   = 0
    self.playlist_id    = 0       # id of the source playlist in database
                                  # 0 = new playlist
    self.name           = "New playlist"
    self.creator        = "Anonymous"
    self.time           = int(time.time())

    self.parent.log.write(log.MESSAGE, "[PLAYLISTMNGR] cleared.")

    # end clear() #

  def load_active_playlist(self):
    """Load last playlist from database"""

    self.parent.led.set_led_yellow(1)
    self.clear()

    connected_revs = {}
    for storid, usb in self.parent.usb.alldevs.iteritems():
      connected_revs[storid] = usb.revision

    entries = []

    for row in self.parent.dbhandle.cur.execute(
        "SELECT usbid, usbrev, dirid, fileid, played FROM Playlistentries "\
        "WHERE playlistid=0 ORDER BY entryin"):
      entries.append(row)

    for row in entries:
      if row[0] in connected_revs and connected_revs[row[0]] == row[1]:
        self.parent.dbhandle.cur.execute("SELECT * FROM Fileentries "\
          "WHERE id=? AND dirid=? AND usbid=?", (row[3], row[2], row[0]))
        fileentry = self.parent.dbhandle.cur.fetchone()
        item = PlayListItem(fileentry, True, row[1])
        item.played = row[4]
        self.playlist.append(item)


      # end for row in Playlistentries #

    self.check_usb_valid()

    self.parent.led.set_led_yellow(0)

    self.parent.log.write(log.MESSAGE,
      "[PLAYLISTMNGR] Loaded active playlist with %d items" %
      len(self.playlist))

    # end load_playlist() #

  def save_active(self):
    """Save current playlist as playlist id 0.

    Called after every change of playlist to recover status after restart
    """

    self.time = int(time.time())

    self.parent.led.set_led_yellow(1)

    self.parent.dbhandle.cur.execute('DELETE FROM Playlists WHERE id=0')
    self.parent.dbhandle.cur.execute(
      'DELETE FROM Playlistentries WHERE playlistid=0')
    self.parent.dbhandle.con.commit()

    self.parent.dbhandle.cur.execute(
        'INSERT INTO Playlists VALUES (?, ?, ?, ?, ?, ?)',
        (0, self.name, self.time, self.creator,
         len(self.playlist), self.playlist_pos))

    pl_items = []
    for i in range(len(self.playlist)):
      self.playlist[i].append_to_db_list(pl_items, self.playlist_id, i)

    self.parent.dbhandle.cur.executemany(
      'INSERT INTO Playlistentries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
      pl_items)

    self.parent.dbhandle.con.commit()
    self.parent.led.set_led_yellow(0)

    # end save_active() #

  def save(self):
    """Write playlist to source playlist in database

    Uses self.playlist_id to identify correct playlist in db.
    Won't work if self.playlist_id == 0 (new playlist)

    Returns True if success, False if id == 0 or failed to write.
    """

    if self.playlist_id == 0 or not len(self.playlist):
      return False

    self.time = int(time.time())

    self.parent.led.set_led_yellow(1)

    self.parent.dbhandle.cur.execute(
        'DELETE FROM Playlists WHERE id=?', (self.playlist_id,))
    self.parent.dbhandle.cur.execute(
        'DELETE FROM Playlistentries WHERE playlistid=?', (self.playlist_id,))
    self.parent.dbhandle.con.commit()

    self.parent.dbhandle.cur.execute(
        'INSERT INTO Playlists VALUES (?, ?, ?, ?, ?, ?)',
        (self.playlist_id, self.name, self.time, self.creator,
         len(self.playlist), self.playlist_pos,))

    pl_items = []
    for i in range(len(self.playlist)):
      self.playlist[i].append_to_db_list(pl_items, self.playlist_id, i)

    self.parent.dbhandle.cur.executemany(
      'INSERT INTO Playlistentries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
      pl_items)

    self.parent.dbhandle.set_settings_value(
      'curplaylist', '%d' % self.playlist_id)

    self.parent.dbhandle.con.commit()

    self.parent.led.set_led_yellow(0)

    self.parent.log.write(log.MESSAGE,
      "[PLAYLISTMNGR]: Saved playlist %s created by %s at %s with length %d " \
      "at position %d as id %d" %
      (self.name, self.creator,
       time.strftime("%x %X", time.localtime(self.time)), len(self.playlist),
       self.playlist_pos, self.playlist_id))

    return True

    # end save() #

  def save_as(self, name, creator):
    """Write new playlist to database

    Returns True if success, False if name exists or failed to write.
    """

    # check if name is unique
    self.parent.dbhandle.cur.execute("SELECT COUNT(name) FROM Playlists "\
      "WHERE name=?;", (name,))
    if self.parent.dbhandle.cur.fetchone()[0] != 0:
      return False

    # get id for new playlist
    new_id = 0
    for row in self.parent.dbhandle.cur.execute(
        "SELECT id FROM Playlists ORDER BY id"):
      new_id = row[0]
    new_id += 1

    self.playlist_id = new_id
    self.name = name
    self.creator = creator

    return self.save()

    # end save_as() #

  def save_overwrite(self, playlist_id):
    """Overwrite existing playlist

    Returns True if success, False if not exists or failed to write.
    """

    # check if id exists
    self.parent.dbhandle.cur.execute("SELECT COUNT(id) FROM Playlists "\
      "WHERE id=?;", (playlist_id,))
    if self.parent.dbhandle.cur.fetchone()[0] != 1:
      return False

    self.parent.dbhandle.cur.execute("SELECT name, creator FROM Playlists "\
      "WHERE id=?;", (playlist_id,))

    row = self.parent.dbhandle.cur.fetchone()

    self.playlist_id = playlist_id
    self.name = row[0]
    self.creator = row[1]

    return self.save()

  def check_usb_valid(self):
    """Check if usb devices for active playlist are connected and revision
    matches

    Drop items not found on USB
    """

    ### TODO implement ###

    # end check_usb_valid() #


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

    self.save_active()
    return True

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

    self.save_active()
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

      for i in range(start_at, min(len(self.playlist), start_at+max_items)):
        res.append(self.playlist[i].print_self(printformat))

    else:
      for row in self.parent.dbhandle.cur.execute(
          "SELECT disptitle FROM Playlistentries ORDER BY entryin LIMIT ? OFFSET ?",
          (max_items, start_at,) ):
        res.append(row[0])

    res[1] = len(res) - 2

    return res

    # end list_playlist() #


  def list_playlists(self):
    '''Cretate list of saved playlists'''

    res = []

    for row in self.parent.dbhandle.cur.execute(
        "SELECT * FROM Playlists ORDER BY id"):

      if row[PL.ID] != 0:
        res.append(u'||%d||%s||%s||%s||%d||' %
                   (row[PL.ID], row[PL.NAME], row[PL.CREATOR],
                    time.strftime("%x %X", time.localtime(row[PL.CREATED])),
                    row[PL.ITEMSCOUNT])
                  )
    return res

    # end list_playlists() #










