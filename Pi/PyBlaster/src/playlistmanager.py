"""playlistmanager.py -- Manage active playlist

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import random
import time

import log
from dbhandle import DBFileEntries as FE


class PlayListManager:
    """
    """

    def __init__(self, parent):
        """Empty ctor

        Need to call load_playlist after other object initialized.
        :param parent: main PyBlaster instance
        """
        random.seed()
        self.parent = parent
        self.playlist_id = 0  # id of the source playlist in database
                              # 0 = new playlist

        # end __init__() #

    def clear(self, list_id=-1):
        """Clean out playlist

        :param list_id: clean playlist #id (0 = current playlist)
        """
        listid = self.get_playlist_id(list_id)
        self.parent.dbhandle.cur.execute(
            "DELETE FROM Playlistentries WHERE playlistid=?", (listid,))
        self.parent.dbhandle.cur.execute(
            "DELETE FROM Playlists WHERE id=?", (listid,))
        self.parent.dbhandle.con.commit()

        self.parent.play.clear_queue()

        # if cleaned playlist was default list, recreate
        if listid == 0:
            self.new_default_playlist()

        self.parent.log.write(log.MESSAGE, "[PLAYLISTMNGR] cleared.")

    def load_active_playlist(self):
        """Load last playlist from database"""

        self.parent.led.set_led_yellow(1)

        # make sure that we have a playlist with id=0
        self.new_default_playlist()

        #connected_revs = {}
        #for storid, usb in self.parent.usb.alldevs.iteritems():
            #connected_revs[storid] = usb.revision

        #entries = []

        #for row in self.parent.dbhandle.cur.execute(
                #"SELECT usbid, usbrev, dirid, fileid, played, path "\
                #"FROM Playlistentries WHERE playlistid=0 ORDER BY position"):
            #entries.append(row)

        #for row in entries:
            #if row[0] not in connected_revs:
                #"""usb device is not connected, insert into playlist,
                #but flag as disabled.
                #"""
                #self.parent.dbhandle.cur.execute("SELECT * FROM Fileentries "\
                    #"WHERE id=? AND dirid=? AND usbid=?",
                    #(row[3], row[2], row[0]))
                #fileentry = self.parent.dbhandle.cur.fetchone()
                #item = PlayListItem(fileentry, False, row[1])
                #item.played = row[4]
                #self.playlist.append(item)
            #if row[0] in connected_revs and connected_revs[row[0]] == row[1]:
                #"""usb device is connected and revision is ok --> file ids
                #have not changed --> may insert item
                #"""
                #self.parent.dbhandle.cur.execute("SELECT * FROM Fileentries "\
                    #"WHERE id=? AND dirid=? AND usbid=?",
                    #(row[3], row[2], row[0]))
                #fileentry = self.parent.dbhandle.cur.fetchone()
                #item = PlayListItem(fileentry, True, row[1])
                #item.played = row[4]
                #self.playlist.append(item)
            #if row[0] in connected_revs and connected_revs[row[0]] != row[1]:
                #"""usb device is connected, but was updated --> check if may
                #insert with new fileentry.
                #"""
                #newrow = self.parent.usb.get_dev_by_storid(row[0]). \
                            #get_fileentry_by_path(row[5])
                #if newrow is not None:
                    #"""found path with new ids"""
                    #item = PlayListItem(newrow, True, connected_revs[row[0]])
                    #item.played = row[4]
                    #self.playlist.append(item)

            ## end for row in Playlistentries #

        #self.parent.led.set_led_yellow(0)

        #self.parent.log.write(log.MESSAGE,
            #"[PLAYLISTMNGR] Loaded active playlist with %d items" %
            #len(self.playlist))

        #self.save_active() # usb revisions may have changed

        # end load_playlist() #

    def new_default_playlist(self):
        """Make sure we have a playlist with id=0, create an empty one if not
        """

        self.parent.dbhandle.cur.execute("SELECT Count() FROM Playlists "
                                         "WHERE id=0")
        res = self.parent.dbhandle.cur.fetchall()
        if int(res[0][0]) == 0:
            self.parent.log.write(log.MESSAGE, "[PLAYLISTMNGR] Generating "
                                               "new empty default playlist...")

            self.parent.dbhandle.cur.execute('INSERT INTO Playlists VALUES ('
                                             '?, ?, ?, ?, ?, ?)',
                                             (0, "Default Playlist",
                                              int(time.time()), "Anonymous",
                                              -1, 0))

            self.parent.dbhandle.con.commit()

    def save_active(self):
        """Save current playlist as playlist id 0.

        Called after every change of playlist to recover status after restart
        """

        #self.time = int(time.time())

        #self.parent.led.set_led_yellow(1)

        #self.parent.dbhandle.cur.execute('DELETE FROM Playlists WHERE id=0')
        #self.parent.dbhandle.cur.execute(
            #'DELETE FROM Playlistentries WHERE playlistid=0')
        #self.parent.dbhandle.con.commit()

        #self.parent.dbhandle.cur.execute(
            #'INSERT INTO Playlists VALUES (?, ?, ?, ?, ?, ?, ?)',
            #(0, self.name, self.time, self.creator,
            #len(self.playlist), self.playlist_pos, 0))

        #pl_items = []
        #for i in range(len(self.playlist)):
            #self.playlist[i].append_to_db_list(pl_items,
                                               #self.playlist_id, i, 0)

        #self.parent.dbhandle.cur.executemany(
            #'INSERT INTO Playlistentries VALUES (?,?,?,?,?,?,?,?,?,?)',
            #pl_items)

        #self.parent.dbhandle.con.commit()
        #self.parent.led.set_led_yellow(0)

        # end save_active() #

    def save(self):
        """Write playlist to source playlist in database

        Uses self.playlist_id to identify correct playlist in db.
        Won't work if self.playlist_id == 0 (new playlist)

        Returns True if success, False if id == 0 or failed to write.
        """

        #if self.playlist_id == 0 or not len(self.playlist):
            #return False

        #self.time = int(time.time())

        #self.parent.led.set_led_yellow(1)

        #self.parent.dbhandle.cur.execute(
                #'DELETE FROM Playlists WHERE id=?', (self.playlist_id,))
        #self.parent.dbhandle.cur.execute(
                #'DELETE FROM Playlistentries WHERE playlistid=?',
                #(self.playlist_id,))
        #self.parent.dbhandle.con.commit()

        #self.parent.dbhandle.cur.execute(
                #'INSERT INTO Playlists VALUES (?, ?, ?, ?, ?, ?, ?)',
                #(self.playlist_id, self.name, self.time, self.creator,
                 #len(self.playlist), self.playlist_pos, 0,))

        #pl_items = []
        #for i in range(len(self.playlist)):
            #self.playlist[i].append_to_db_list(pl_items, self.playlist_id,
            # i,0)

        #self.parent.dbhandle.cur.executemany(
            #'INSERT INTO Playlistentries VALUES (?,?,?,?,?,?,?,?,?,?)',
            #pl_items)

        #self.parent.dbhandle.set_settings_value(
            #'curplaylist', '%d' % self.playlist_id)

        #self.parent.dbhandle.con.commit()

        #self.parent.led.set_led_yellow(0)

        #self.parent.log.write(log.MESSAGE,
            #"[PLAYLISTMNGR]: Saved playlist %s created by %s at %s with " \
            #" length %d at position %d as id %d" %
            #(self.name, self.creator,
             #time.strftime("%x %X", time.localtime(self.time)),
             #len(self.playlist), self.playlist_pos, self.playlist_id))

        #return True

        # end save() #

    def save_as(self, name, creator):
        """Write new playlist to database

        Returns True if success, False if name exists or failed to write.
        """

        ## check if name is unique
        #self.parent.dbhandle.cur.execute("SELECT COUNT(name) FROM Playlists "\
            #"WHERE name=?;", (name,))
        #if self.parent.dbhandle.cur.fetchone()[0] != 0:
            #return False

        ## get id for new playlist
        #new_id = 0
        #for row in self.parent.dbhandle.cur.execute(
                #"SELECT id FROM Playlists ORDER BY id"):
            #new_id = row[0]
        #new_id += 1

        #self.playlist_id = new_id
        #self.name = name
        #self.creator = creator

        #return self.save()

        # end save_as() #

    def save_overwrite(self, playlist_id):
        """Overwrite existing playlist

        Returns True if success, False if not exists or failed to write.
        """

        ## check if id exists
        #self.parent.dbhandle.cur.execute("SELECT COUNT(id) FROM Playlists "\
            #"WHERE id=?;", (playlist_id,))
        #if self.parent.dbhandle.cur.fetchone()[0] != 1:
            #return False

        #self.parent.dbhandle.cur.execute("SELECT name, creator FROM " \
            #" Playlists WHERE id=?;", (playlist_id,))

        #row = self.parent.dbhandle.cur.fetchone()

        #self.playlist_id = playlist_id
        #self.name = row[0]
        #self.creator = row[1]

        #return self.save()

    def usb_removed(self, storid):
        """Called by UsbDevice.release() if usb device got lost

        Disable playlist items by flagging is_connected with False
        """

        # TODO if playing song from this USB, skip to next valid track

        self.parent.play.requeue()

        #if not self.playlist:
            #return

        #disabled = 0
        #for item in self.playlist:
            #disabled += item.set_connected_by_storid(storid, False)

        #self.parent.log.write(log.MESSAGE,
            #"[PLAYLISTMNGR]: USB #%d got removed, disabled %d items " \
            #"in playlist" % (storid, disabled))

        # end usb_removed() #

    def usb_connected(self, storid, revision, usbdev):
        """Called by UsbDevice.__init__() after device is loaded.

        Flag playlist items on this device as valid.
        Check if items still on drive.
        """

        self.parent.play.requeue()

        #if not self.playlist:
            #return

        #self.parent.led.set_led_yellow(1)

        #enabled = 0
        #dropped = 0

        #tmp_list = self.playlist
        #self.playlist = []

        #for item in tmp_list:
            #if item.check_revision_matches(revision, usbdev):
                #self.playlist.append(item)
                #enabled += item.set_connected_by_storid(storid, True)
            #else:
                #dropped += 1

        #self.parent.log.write(log.MESSAGE,
            #"[PLAYLISTMNGR]: USB #%d got connected, enabled %d items in " \
            #"playlist and dropped %d items." % (storid, enabled, dropped))

        #self.save_active()

        #self.parent.led.set_led_yellow(0)

        # end usb_connected() #

    def list_playlist(self,
                      list_id=0,
                      start_at=0,
                      max_items=100,
                      printformat=0):
        """Show current playlist

        :param list_id: print playlist #id (0 = current playlist)
        :param start_at: start displaying at position N
        :param max_items: do not show more than N items
        :param printformat: unused now
        :returns string list: [[..,..,..]]
        """

        connected_usbs = self.parent.usb.connected_usbids()
        if not connected_usbs:
            return []

        usb_list = ",".join(map(str, connected_usbs))
        statement = "SELECT position, played, disptitle FROM " \
                    "Playlistentries " \
                    "WHERE playlistid=%d AND usbid IN (%s) AND position>=%d " \
                    "ORDER BY position LIMIT %d" % \
                    (list_id, usb_list, start_at, max_items)

        res = []
        current_pos = self.get_playlist_position(list_id)
        for row in self.parent.dbhandle.cur.execute(statement):
            played = 2 if row[0] == current_pos else row[1]
            res.append(['%d' % row[0],
                        '%d' % played,
                        row[2]])
        return res

        # end list_playlist() #

    def list_playlists(self):
        """Cretate list of saved playlists"""

        #res = []

        #for row in self.parent.dbhandle.cur.execute(
                #"SELECT * FROM Playlists ORDER BY id"):

            #if row[PL.ID] != 0:
                #res.append(u'||%d||%s||%s||%s||%d||' %
                           #(row[PL.ID], row[PL.NAME], row[PL.CREATOR],
                            #time.strftime("%x %X",
                                          #time.localtime(row[PL.CREATED])),
                            #row[PL.ITEMSCOUNT]))
        #return res

        # end list_playlists() #

    def get_playlist_id(self, list_id=-1):
        if list_id == -1:
            return self.playlist_id
        return list_id

    def get_playlist_state(self, listid=-1):
        """Latest state for playlist to have undo actions in playlist
        """
        listid = self.get_playlist_id(listid)
        self.parent.dbhandle.cur.execute(
            "SELECT state FROM Playlists WHERE id=?", (listid,))
        # there should be a row, so no check
        res = self.parent.dbhandle.cur.fetchall()
        if len(res) == 0:
            return -1
        return int(res[0][0])

    def get_playlist_position(self, listid=-1):
        """Current position pointer in playlist.
        :param listid: id of playlist, default = -1 -> use active playlist
        :returns: Position pointer for playlist
                (-1 if no such playlist, -1 if pointer not set for playlist)
        :rtype: int
        """
        listid = self.get_playlist_id(listid)
        self.parent.dbhandle.cur.execute(
            "SELECT position FROM Playlists WHERE id=?", (listid,))
        # there should be a row, so no check
        res = self.parent.dbhandle.cur.fetchall()
        if len(res) == 0 or res[0][0] is None:
            return -1
        return int(res[0][0])

    def get_last_playlist_position(self, listid=-1):
        """Return position index of last item in playlist.
        :param listid: id of playlist, default = -1 -> use active playlist
        :returns: Last position index in playlist
                (-1 if no such playlist, -1 if pointer not set for playlist)
        :rtype: int
        """
        listid = self.get_playlist_id(listid)
        self.parent.dbhandle.cur.execute(
            "SELECT Max(position) FROM Playlistentries WHERE playlistid=?",
            (listid,))
        # there should be a row, so no check
        res = self.parent.dbhandle.cur.fetchall()
        if len(res) == 0 or res[0][0] is None:
            return -1
        return int(res[0][0])

    def get_next_two_playlist_positions(self, listid=-1):
        """Get current position from playlist and position number of next song

        :param listid: id of playlist, default = -1 -> use active playlist
        :returns: [] if no playlist, [pos1] if last item or
            only 1 item in list or [pos1,pos2].
        :rtype: [int]
        """
        connected_usbs = self.parent.usb.connected_usbids()
        if not connected_usbs:
            return []

        listid = self.get_playlist_id(listid)
        position = self.get_playlist_position(listid)

        usb_list = ",".join(map(str, connected_usbs))

        # TODO if repeat all, add first position if only 1 row
        statement = "SELECT position FROM Playlistentries " \
                    "WHERE playlistid=%d AND usbid IN (%s) AND position>=%d " \
                    "ORDER BY position LIMIT 2" % \
                    (listid, usb_list, position)
        ret = []
        for row in self.parent.dbhandle.cur.execute(statement):
            ret.append(row[0])
        return ret

    def get_filename_from_playlist(self, list_id, position):
        """Get filename for item in playlist with position

            Select next item in playlist with position >= position.

            :param list_id: playlist id
            :param position: position pointer in playlist
            :returns: path of item in playlist or None if wrong args
            :rtype: None or str
            """
        self.parent.dbhandle.cur.execute(
            "SELECT usbid, path FROM Playlistentries WHERE playlistid=? "
            "AND position=?", (list_id, position))
        res = self.parent.dbhandle.cur.fetchall()
        if len(res) == 0:
            return None
        usbdev = self.parent.usb.get_dev_by_storid(res[0][0])
        if usbdev is None:
            return None
        return usbdev.mnt_pnt + "/" + res[0][1]

    def get_current_tune_info(self, listid=-1):
        """

        """
        listid = self.get_playlist_id(listid)
        position = self.get_playlist_position(listid)

        self.parent.dbhandle.cur.execute(
            "SELECT Fileentries.* "
            "FROM Playlistentries, Fileentries "
            "WHERE "
            "Playlistentries.playlistid=? AND "
            "Playlistentries.position=? AND "
            "Fileentries.id=Playlistentries.fileid AND "
            "Fileentries.dirid=Playlistentries.dirid AND "
            "Fileentries.usbid=Playlistentries.usbid", (listid, position))

        res = self.parent.dbhandle.cur.fetchall()
        if len(res) == 0:
            return None

        return [
            "%d" % res[0][FE.ID],
            "%d" % res[0][FE.DIRID],
            "%d" % res[0][FE.STORID],
            res[0][FE.TITLE],
            res[0][FE.ALBUM],
            res[0][FE.ARTIST],
            res[0][FE.GENRE],
            "%d" % res[0][FE.YEAR],
            "%d" % position
        ]

    def get_playlist_last_position(self, listid=-1):
        """Latest state for playlist to have undo actions in playlist
        """
        if listid == -1:
            listid = self.playlist_id
        self.parent.dbhandle.cur.execute(
            "SELECT MAX(position) FROM Playlistentries WHERE playlistid=?",
            (listid,))
        # there should be a row, so no check
        res = self.parent.dbhandle.cur.fetchall()[0][0]
        if res is None:
            return -1
        return int(res)

    def set_playlist_state(self, listid, state):
        """Set current state for playlist for undo actions
        """
        self.parent.dbhandle.cur.execute(
            "UPDATE Playlists SET state=? WHERE id=?", (state, listid))
        self.parent.dbhandle.con.commit()

    def append_multiple(self, add_instructions, add_mode):
        """Called on plappendmultiple with payload instructions
        """

        list_id = 0
        append_list = []

        self.parent.led.set_led_yellow(1)

        # append_file() wastes database pointer, so we need to
        # create a list first (read-only) and then append
        # items to playlist
        for line in add_instructions:
            instruction = line.split(' ')
            if instruction[0] == 'DIR':
                stor_id = int(instruction[1])
                dir_id = int(instruction[2])
                self.scan_dir(append_list, list_id, stor_id, dir_id)
            elif instruction[0] == 'FILE':
                stor_id = int(instruction[1])
                dir_id = int(instruction[2])
                file_id = int(instruction[3])
                append_list.append([stor_id, dir_id, file_id])
            else:
                self.parent.log.write(log.ERROR, "[PLAYLISTMNGR]: Unknown "
                                                 "add command %s in "
                                                 "append_multiple()" %
                                                 (instruction[0]))

        added = self.multi_append(list_id, append_list, add_mode)
        self.parent.led.set_led_yellow(0)
        self.parent.play.requeue()

        return added

        # end append_multiple() #

    def modify_playlist(self, instructions, mod_mode):
        """

        """

        mod_list = []
        cur_pos = self.get_playlist_position()
        for line in instructions:
            inst = line.split(' ')
            pos = int(inst[1])
            # do not insert current tune, will waste playlist!
            if pos != cur_pos:
                mod_list += [pos]

        if mod_mode == 1:
            self.delete_from_playlist(mod_list)
        if mod_mode == 2:
            self.move_items_after_current(mod_list)
        if mod_mode == 3:
            self.move_items_to_end(mod_list)

    def delete_from_playlist(self, pos_list, list_id=-1):
        """

        """

        if list_id == -1:
             list_id = self.playlist_id
        if len(pos_list) == 0:
            return

        pos = ",".join(map(str, pos_list))
        statement = "DELETE FROM Playlistentries WHERE playlistid=%d AND " \
                    "position in (%s)" % (list_id, pos)

        self.parent.dbhandle.cur.execute(statement)
        self.parent.dbhandle.con.commit()
        self.parent.play.requeue()

    def move_items_to_end(self, pos_list, list_id=-1):
        """

        """
        if list_id == -1:
             list_id = self.playlist_id
        if len(pos_list) == 0:
            return

        pos = ",".join(map(str, pos_list))
        pos_offset = self.get_playlist_last_position(list_id) - pos_list[0]+1
        statement = "UPDATE Playlistentries SET position=position+%d WHERE " \
                    "playlistid=%d AND position IN (%s)" % \
                    (pos_offset, list_id, pos)

        self.parent.dbhandle.cur.execute(statement)
        self.parent.dbhandle.con.commit()
        self.parent.play.requeue()

    def move_items_after_current(self, pos_list, list_id=-1):
        """

        """
        if list_id == -1:
             list_id = self.playlist_id
        if len(pos_list) == 0:
            return

        pos = ",".join(map(str, pos_list))
        cur_pos = self.get_playlist_position(list_id)
        pos_offset = cur_pos - pos_list[0] + 1
        pos_offset_other = pos_list[-1] - pos_list[0] + 1

        self.parent.log.write(log.DEBUG1,
                              "--- move: cur_pos=%d, pos_off=%d, "
                              "pos_off2=%d, pos=%s" % (cur_pos, pos_offset,
                                                       pos_offset_other, pos))

        # hide selected items while moving using sign and -1 to include 0
        statement = "UPDATE Playlistentries SET position=position*-1-1 " \
                    "WHERE playlistid=%d AND position IN (%s)" % (list_id, pos)
        self.parent.log.write(log.DEBUG1, statement)
        self.parent.dbhandle.cur.execute(statement)
        self.parent.dbhandle.con.commit()

        # increase position of all unselected items behind current by
        # selected range + 1
        statement = "UPDATE Playlistentries SET position=position+%d WHERE " \
                    "playlistid=%d AND position NOT IN (%s) AND position > " \
                    "%d" % (pos_offset_other, list_id, pos, cur_pos)
        self.parent.log.write(log.DEBUG1, statement)
        self.parent.dbhandle.cur.execute(statement)
        self.parent.dbhandle.con.commit()

        # increase position of selected items to be placed behind
        # current item and undo * -1 - 1, selected items are < 0
        statement = "UPDATE Playlistentries SET position=(position+1)*-1+%d " \
                    "WHERE playlistid=%d AND position < 0" % \
                    (pos_offset, list_id)
        self.parent.log.write(log.DEBUG1, statement)
        self.parent.dbhandle.cur.execute(statement)
        self.parent.dbhandle.con.commit()
        self.parent.play.requeue()

    def scan_dir(self, app_list, list_id, stor_id, dir_id):
        """
        """
        # need to copy subdirs to list, because recursion will break DB cursor
        sub_dirs = []
        for row in self.parent.dbhandle.cur.execute(
                "SELECT id FROM Dirs WHERE usbid=? AND parentid=? ORDER BY id",
                (stor_id, dir_id)):
            sub_dirs += row

        # dive into sub dirs
        for item in sub_dirs:
            self.scan_dir(app_list, list_id, stor_id, item)

        for row in self.parent.dbhandle.cur.\
                execute("SELECT id FROM ""Fileentries WHERE usbid=? AND "
                        "dirid=? ORDER BY id", (stor_id, dir_id)):
            app_list.append([stor_id, dir_id, row[0]])

    def multi_append(self, list_id, id_list, add_mode):
        """
        """
        if len(id_list) == 0:
            return

        self.parent.led.set_led_yellow(1)
        state = self.get_playlist_state(list_id) + 1

        if add_mode == 1:
            # insert after current, raise position numbers for
            # items with index above insertion point
            insert_pos = self.get_playlist_position(list_id) + 1
            insert_count = len(id_list)
            self.parent.dbhandle.cur.\
                execute("UPDATE Playlistentries set position=position+? "
                        "WHERE playlistid=? AND position>=?",
                        (insert_count, list_id, insert_pos))
        else:
            insert_pos = self.get_playlist_last_position(list_id) + 1

        for item in id_list:
            self.parent.dbhandle.cur.\
                execute("SELECT path, disptitle FROM Fileentries WHERE "
                        "usbid=? AND dirid=? AND id=?", (item[0], item[1],
                                                         item[2],))
            res = self.parent.dbhandle.cur.fetchall()
            if len(res) == 0:
                # TODO error file not found in DB
                continue
            path = res[0][0]
            title = res[0][1]

            self.parent.dbhandle.cur.execute(
                "INSERT INTO Playlistentries VALUES (?,?,?,?,?,?,?,?,?,?)",
                (list_id, insert_pos, item[0],
                 self.parent.usb.revision(item[0]),
                 item[1], item[2], title, 0, path, state))
            insert_pos += 1

        self.set_playlist_state(list_id, state)

        self.parent.dbhandle.con.commit()
        self.parent.led.set_led_yellow(0)

        self.parent.log.write(log.ERROR, "[PLAYLISTMNGR]: Added %d items for "
                                         "playlist %d with state %d" %
                                         (len(id_list), list_id, state))
        self.parent.play.requeue()

        return len(id_list)

        # end multi_append() #

    def randomize_playlist(self, mode, list_id=-1):
        """

        :param mode: (2=randomize whole playlist, 1=(pos+1, end)

        """
        if list_id == -1:
            list_id = self.playlist_id

        # start randomizing from position >= seek_pos
        start_pos = 0
        seek_pos = 0
        cur_pos = self.get_playlist_position(list_id)
        if mode == 1:
            start_pos = cur_pos
            seek_pos = start_pos+1

        # remember current tune
        self.parent.dbhandle.cur.execute(
            "SELECT path FROM Playlistentries WHERE playlistid=? "
            "AND position=?", (list_id, cur_pos))
        cur_path = None
        res = self.parent.dbhandle.cur.fetchall()
        if len(res) > 0 and res[0][0] is not None:
            cur_path = res[0][0]
            self.parent.log.write(log.DEBUG1, "----"+cur_path)

        # get random positions and update positions in playlist with -sign
        new_pos = seek_pos
        update_pos = {}
        for row in self.parent.dbhandle.cur.execute(
                "SELECT position FROM Playlistentries WHERE playlistid=? "
                "AND position>=? ORDER BY RANDOM()",
                (list_id, seek_pos)):
            update_pos[int(row[0])] = new_pos
            new_pos += 1

        for old_pos, new_pos in update_pos.iteritems():
            self.parent.log.write(log.DEBUG1, "%d -> %d" % (old_pos, new_pos))
            self.parent.dbhandle.cur.execute(
                "UPDATE Playlistentries SET position=-? WHERE position=? AND "
                "playlistid=?", (new_pos, old_pos, list_id))
        self.parent.dbhandle.con.commit()

        # revert sign
        self.parent.dbhandle.cur.execute(
                "UPDATE Playlistentries SET position=-position "
                "WHERE position<0 AND playlistid=?", (list_id,))
        self.parent.dbhandle.con.commit()

        # reset position pointer in mode all
        if mode != 1:
            new_pos = 0
            if cur_path is not None:
                self.parent.dbhandle.cur.execute(
                    "SELECT position FROM Playlistentries WHERE playlistid=? "
                    "AND path=?", (list_id, cur_path))
                res = self.parent.dbhandle.cur.fetchall()[0][0]
                self.parent.log.write(log.DEBUG1, "----%d" % res)
                if res is not None:
                    new_pos = int(res)
            self.set_position_pointer(list_id, new_pos)
        else:
            new_pos = start_pos  # position not changed in mode 1

        self.parent.play.requeue()

        self.parent.log.write(log.MESSAGE,
                              "Playlist randomized mode %d, start_pos=%d, "
                              "new_cur_pos=%d" % (mode, start_pos, new_pos))

        # end randomize_playlist() #

    def set_position_pointer(self, list_id=-1, position=-1):
        """Set current playlist position in database

        :param list_id: playlist to set position pointer for (default=current)
        :param position: new playlist position (current song)
        """
        if list_id == -1:
            list_id = self.playlist_id

        self.parent.dbhandle.cur.execute(
            "UPDATE Playlists SET position=? WHERE id=?", (position, list_id))
        self.parent.dbhandle.con.commit()

    def get_prev_position_in_playlist(self, listid=-1):
        """
        """
        listid = self.get_playlist_id(listid)
        self.parent.dbhandle.cur.execute(
            "SELECT Playlistentries.position FROM Playlistentries, Playlists "
            "WHERE Playlistentries.position < Playlists.position AND "
            "Playlists.id=?  ORDER BY Playlistentries.position DESC LIMIT 1",
            (listid,))
        res = self.parent.dbhandle.cur.fetchall()
        if len(res) == 0:
            return -1
        return int(res[0][0])

    def get_next_position_in_playlist(self, listid=-1):
        """
        """
        listid = self.get_playlist_id(listid)
        self.parent.dbhandle.cur.execute(
            "SELECT Playlistentries.position FROM Playlistentries, Playlists "
            "WHERE Playlistentries.position > Playlists.position AND "
            "Playlists.id=?  ORDER BY Playlistentries.position LIMIT 1",
            (listid,))
        res = self.parent.dbhandle.cur.fetchall()
        if len(res) == 0:
            return -1
        return int(res[0][0])
