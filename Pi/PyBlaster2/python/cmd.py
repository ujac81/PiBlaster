"""cmd.py -- Evaluate commands received via RFCOMM, Lirc or Buttons

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from codes import *

import gpio
import log


STATUSOK = 0            # evaluation successful
ERRORPARSE = 1          # failed to read command
ERRORUNKNOWN = 2        # unknown command
ERRORARGS = 3           # wrong number or wrong type of args
ERROREVAL = 4           # evaluation did not succeed,
                        # because called function failed

STATUSEXIT = 100        # tell calling instance to close comm/pipe/whatever
STATUSDISCONNECT = 101  # tell calling instance to close comm/pipe/whatever


class Cmd:
    """ Evaluate commands reveived via RFCOMM or pipe"""

    def __init__(self, main):
        """ Set in/out fifos to None"""

        self.main = main

    def eval(self, cmdline, src='Unknown', payload=None):
        """Evaluate command and perform action

        Called by RFCommServer, Lirc or Buttons

        :returns [status, code, status_msg, result_list]
        """
        cmdline = cmdline.strip()
        line = cmdline.split()
        line = [s.replace("_", " ") for s in line]
        cmd = ""
        if line:
            cmd = line[0]

        int_args = []
        for args in line:
            try:
                intarg = int(args)
                int_args.append(intarg)
            except TypeError:
                int_args.append(None)
            except ValueError:
                int_args.append(None)

        ret_stat = STATUSOK
        ret_msg = "OK"
        ret_code = -1
        ret_list = []

        if payload is None:
            payload = []

        self.main.log.write(log.MESSAGE,
                            "Eval cmd [%s]: %s; payload size: %d" %
                            (src, " || ".join(line), len(payload)))

        # Command evaluation, in alphabetical order.

        # # # # disconnect # # # #

        if cmd == "disconnect":
            ret_stat = STATUSDISCONNECT

        # # # # lsfulldir <storid> <dirid> # # # #

        # elif cmd == "lsfulldir":
        #     if len(line) != 3:
        #         ret_stat = ERRORARGS
        #         ret_msg = "lsfulldir needs 2 args"
        #     else:
        #         stor = self.parent.usb.get_dev_by_storid(int_args[1])
        #         if stor is None:
        #             ret_stat = ERRORARGS
        #             ret_msg = "illegal storage id"
        #         else:
        #             ret_list = stor.list_full_dir(int_args[2])
        #             ret_code = LS_FULL_DIR

        # # # # keepalive # # # #

        elif cmd == "keepalive":
            # nothing to do, timeout poll count will be reset
            # in RFCommServer.read_command()
            ret_msg = "OK"
            ret_code = KEEP_ALIVE

        # # # # plappendmultiple # # # #

        # elif cmd == "plappendmultiple":
        #     if len(line) != 2 or int_args[1] is None:
        #         ret_stat = ERRORARGS
        #         ret_msg = "plappendmultiple needs 2 args"
        #     elif src != 'rfcomm':
        #         ret_stat = ERROREVAL
        #         ret_msg = "plappendmultiple need to be called via BT"
        #     else:
        #         added = self.parent.listmngr.append_multiple(payload,
        #                                                      int_args[1])
        #         ret_msg = "%d items appended to playlist" % added
        #         ret_code = PL_ADD_OK

        # # # # playnext # # # #

        # elif cmd == "playnext":
        #
        #     self.parent.play.play_next()
        #     self.parent.play.send_track_info()
        #     ret_code = PLAY_NEXT

        # # # # playpause # # # #

        # elif cmd == "playpause":
        #     # pause / unpause or start playing at current playlist pos
        #
        #     self.parent.play.play_pause()
        #     self.parent.play.send_track_info()
        #     ret_code = PLAY_PAUSE

        # # # # playprev # # # #

        # elif cmd == "playprev":
        #
        #     self.parent.play.play_prev()
        #     self.parent.play.send_track_info()
        #     ret_code = PLAY_PREV

        # # # # playstatus # # # #

        # elif cmd == "playstatus":
        #     # show current playlist item
        #
        #     info = self.parent.play.get_play_status()
        #     if info is None:
        #         ret_stat = -1
        #     else:
        #         ret_list = [info]
        #     ret_code = PLAY_INFO

        # # # # plclear # # # #

        # elif cmd == "plclear":
        #     if len(line) == 2 and int_args[1] is not None:
        #         self.parent.listmngr.clear(int_args[1])
        #     else:
        #         self.parent.listmngr.clear()
        #     ret_msg = "Playlist cleared."

        # # # # plgoto # # # #

        # elif cmd == "plgoto":
        #     if len(line) == 3 and int_args[1] is not None and \
        #             int_args[2] is not None:
        #         self.parent.play.load(int_args[1], int_args[2])
        #         ret_code = PL_JUMP_OK
        #         self.parent.play.send_track_info()
        #     elif len(line) == 2 and int_args[1] is not None:
        #         self.parent.play.load(-1, int_args[1])
        #         ret_code = PL_JUMP_OK
        #         self.parent.play.send_track_info()

        # # # #  plmodify # # # #

        # elif cmd == "plmodify":
        #     if len(line) == 2 and int_args[1] is not None:
        #         self.parent.listmngr.modify_playlist(payload, int_args[1])
        #         ret_msg = "OK"
        #         ret_code = PL_MODIFIED
        #     else:
        #         ret_stat = ERRORARGS
        #         ret_msg = "plmodify needs 1 int arg!"

        # # # # plsave # # # #

        # elif cmd == "plsave":
        #     if not self.parent.listmngr.save():
        #         ret_stat = ERROREVAL
        #         ret_msg = "Save failed -- name exists or playlist empty!"
        #     else:
        #         ret_msg = "Playlist saved."

        # # # # plsaveas # # # #

        # elif cmd == "plsaveas":
        #     if len(line) != 3:
        #         ret_stat = ERRORARGS
        #         ret_msg = "plsaveas needs 2 args!"
        #     else:
        #         if not self.parent.listmngr.save_as(line[1], line[2]):
        #             ret_stat = ERROREVAL
        #             ret_msg = "Save failed -- name exists or playlist empty!"
        #         else:
        #             ret_msg = "Playlist saved as %s." % line[1]

        # # # # plsaveasexisting # # # #

        # elif cmd == "plsaveasexisting":
        #     if len(line) != 2 or int_args[1] is None:
        #         ret_stat = ERRORARGS
        #         ret_msg = "plsaveasexisting needs 1 arg!"
        #     else:
        #         if not self.parent.listmngr.save_overwrite(int_args[1]):
        #             ret_stat = ERROREVAL
        #             ret_msg = \
        #                 "Save failed -- no such playlist or playlist empty!"
        #         else:
        #             ret_msg = "Playlist %d overwitten." % int_args[1]

        # # # # plshow # # # #

        # elif cmd == "plshow":
        #     if len(line) != 5 or int_args[1] is None or \
        #             int_args[2] is None or int_args[3] is None or \
        #             int_args[4] is None:
        #         ret_stat = ERRORARGS
        #         ret_msg = "plshow needs 4 args"
        #     else:
        #         ret_list = self.parent.listmngr.list_playlist(
        #             list_id=int_args[1],
        #             start_at=int_args[2],
        #             max_items=int_args[3],
        #             printformat=line[4])
        #         ret_msg = "OK"
        #         ret_code = PL_SHOW

        # # # # plshowlists # # # #

        # elif cmd == "plshowlists":
        #     ret_list = self.parent.listmngr.list_playlists()

        # # # # plrandomize # # # #

        # elif cmd == "plrandomize":
        #     if len(line) != 2 or int_args[1] is None:
        #         ret_stat = ERRORARGS
        #         ret_msg = "plrandomize 1|2"
        #     else:
        #         self.parent.listmngr.randomize_playlist(int_args[1])
        #         ret_msg = "OK"
        #         ret_code = PL_MODIFIED

        # # # # poweroff # # # #

        elif cmd == "poweroff":
            ret_stat = STATUSEXIT
            self.main.keep_run = 0
            self.main.ret_code = 10  # tell init script to invoke poweroff

        # # # # quit # # # #

        elif cmd == "quit":
            ret_stat = STATUSEXIT
            self.main.keep_run = 0

        # # # # search # # # #

        # elif cmd == "search":
        #     if len(line) < 4:
        #         ret_stat = ERRORARGS
        #         ret_msg = "search needs 3+ args"
        #     elif int_args[1] is None or int_args[2] is None:
        #         ret_stat = ERRORARGS
        #         ret_msg = "Usage: search MODE LIMIT PATTERN"
        #     else:
        #         pattern = ' '.join(line[3:])
        #         ret_list = self.parent.usb.search_files(pattern, int_args[1],
        #                                                 int_args[2])
        #         ret_code = SEARCH_RES

        # # # # vol_dec / vol_inc # # # #

        # elif cmd == "voldec" or cmd == "volinc":
        #     vol_change = self.parent.settings.default_vol_change
        #
        #     if len(line) == 2 and int_args[1] is not None:
        #         vol_change = int_args[1]
        #
        #     if cmd == "voldec":
        #         self.parent.play.vol_dec(vol_change)
        #     else:
        #         self.parent.play.vol_inc(vol_change)
        #
        #     # let APP set correct volume slider position
        #     self.parent.play.send_track_info()

        # # # # vol_set # # # #

        # elif cmd == "volset":
        #     if len(line) != 2:
        #         ret_stat = ERRORARGS
        #         ret_msg = "volset needs 1 arg"
        #     else:
        #         if int_args[1] is None:
        #             ret_stat = ERRORARGS
        #             ret_msg = "volsset needs int arg"
        #         else:
        #             self.parent.play.vol_set(int_args[1])
        #             # let APP set correct volume slider position
        #             self.parent.play.send_track_info()

        else:
            ret_stat = ERRORUNKNOWN
            ret_msg = "unknown command"

        self.main.log.write(log.MESSAGE, ">>> %s" % ret_msg)

        if src != 'button' and ret_stat != STATUSEXIT:
            if ret_stat == STATUSOK:
                self.main.led.flash_led(gpio.LED_WHITE, 1.0)
            else:
                self.main.led.flash_led(gpio.LED_RED, 1.0)

        return [ret_stat, ret_code, ret_msg, ret_list]
