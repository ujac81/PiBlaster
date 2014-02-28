"""play.py -- Play tunes

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import pygame

import codes
import log
import rfcommserver

SONG_END = pygame.USEREVENT + 1


class Play:
    """
    """

    def __init__(self, parent):
        """Empty ctor

        Need to call load_playlist after other object initialized.
        :param parent: main PyBlaster instance
        """
        assert isinstance(parent, object)
        self.parent = parent

        self.init_mixer()
        self.pause = False

        # end __init__() #

    @staticmethod
    def init_mixer():
        """

        """
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(SONG_END)

    def play_pause(self):
        """

        """
        if pygame.mixer.music.get_busy():
            if self.pause:
                pygame.mixer.music.unpause()
                self.pause = False
                return 11
            else:
                pygame.mixer.music.pause()
                self.pause = True
                return 10
        else:
            return self.load()  # -1, 1 or 2

    def play_next(self):
        """
        """
        pos = self.parent.listmngr.get_next_position_in_playlist()
        if pos != -1:
            self.load(-1, pos)

    def play_prev(self):
        """
        """
        pos = self.parent.listmngr.get_prev_position_in_playlist()
        if pos != -1:
            self.load(-1, pos)

    def load(self, list_id=-1, pl_pos=-1):
        """Load and play song from playlist and queue next song

        Call to directly play from playlist.

        :param list_id: playlist id, default = current playlist
        :param pl_pos: playlist position (-1 = current position)
        :returns: -1 on any error, 1 if playing,
                  2 if playing and next song queued.
        """

        self.pause = False

        list_id = self.parent.listmngr.get_playlist_id(list_id)
        if pl_pos != -1:
            self.parent.listmngr.set_position_pointer(list_id, pl_pos)
        positions = self.parent.listmngr.\
            get_next_two_playlist_positions(list_id)

        if len(positions) == 0:
            self.parent.log.write(log.MESSAGE,
                                  "[PLAY]: No tunes in playlist, so not "
                                  "playing!")
            return -1  # no positions found (no playlist?)

        file = self.parent.listmngr.\
            get_filename_from_playlist(list_id, positions[0])
        if file is None:
            return -1  # failed to load song (should not happen)

        self.parent.log.write(log.MESSAGE,
                              "[PLAY]: Loading: %s @ pos %d" %
                              (file, positions[0]))
        self.parent.listmngr.set_position_pointer(list_id, positions[0])

        failed = False
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
        except pygame.error as e:
            self.parent.log.write(log.ERROR,
                                  "[PLAY]: Cannot load %s: %s" %
                                  (file, e.args[0]))
            failed = True

        if failed and len(positions) > 1:
            # advance one position in playlist if tune failed to play.
            # WARNING, this is a exception-induced recursion.
            return self.load(list_id, positions[1])

        if len(positions) == 1:
            return 1

        # Try to queue next song, if queuing fails, do nothing.
        # End event handler will try to load next song.
        file = self.parent.listmngr.\
            get_filename_from_playlist(list_id, positions[1])
        if file is None:
            return 1  # failed to queue next song (should not happen)
        try:
            pygame.mixer.music.queue(file)
        except pygame.error as e:
            self.parent.log.write(log.ERROR,
                                  "[PLAY]: Cannot queue %s: %s" %
                                  (file, e.args[0]))
            return 1  # 1st song added successfully
        self.parent.log.write(log.MESSAGE,
                              "[PLAY]: Queued: %s @ pos %d" %
                              (file, positions[1]))

        return 2

    def check_pygame_events(self):
        """

        """

        for event in pygame.event.get():
            if event.type == SONG_END:
                self.parent.log.write(log.MESSAGE, "[PLAY]: Song ended.")
                self.advance_in_playlist()
                self.send_track_info()

    def advance_in_playlist(self):
        """
        """
        list_id = self.parent.listmngr.get_playlist_id()
        positions = self.parent.listmngr.get_next_two_playlist_positions()
        if len(positions) < 2:
            return  # there are no more items in playlist -- leave

        # set position pointer to 2nd position
        self.parent.listmngr.set_position_pointer(list_id, positions[1])

        # get next 2 positions
        positions = self.parent.listmngr.get_next_two_playlist_positions()
        if len(positions) < 2:
            return  # there are no more items in playlist -- leave

        # Try to queue next song, if queuing fails, do nothing.
        # End event handler will try to load next song.
        file = self.parent.listmngr.\
            get_filename_from_playlist(list_id, positions[1])
        if file is None:
            return
        try:
            pygame.mixer.music.queue(file)
        except pygame.error as e:
            self.parent.log.write(log.ERROR,
                                  "[PLAY]: Cannot queue %s: %s" %
                                  (file, e.args[0]))
            return
        self.parent.log.write(log.MESSAGE,
                              "[PLAY]: Queued: %s @ pos %d" %
                              (file, positions[1]))

        # end advance_in_playlist() #

    def get_play_status(self):
        """

        [0:busy, pos, pause, id, dirid, storid,
         6:title, album, artist, genre, year]

        """
        info = self.parent.listmngr.get_current_tune_info()
        if info is None:
            return None
        pos = 0
        busy = pygame.mixer.music.get_busy()
        if busy:
            pos = pygame.mixer.music.get_pos()
        return ["%d" % busy, "%d" % pos, "%d" % self.pause] + info

    def send_track_info(self):
        """

        """
        if self.parent.rfcomm.mode != rfcommserver.AUTHORIZED:
            return

        info = self.get_play_status()
        ret_status = 0
        ret_code = codes.PLAY_INFO
        ret_msg = "OK"
        if info is None:
            ret_status = -1
            info = []
            ret_msg = "Nothing to play: playlist empty or broken file"
        self.parent.rfcomm.send_client(-1, ret_status, ret_code,
                                       ret_msg, [info])
