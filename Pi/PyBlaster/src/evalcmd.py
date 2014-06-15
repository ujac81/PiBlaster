"""evalcmd.py -- Evaluate commands reveived via RFCOMM or pipe

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import codecs
import os

from codes import *
import led
import log
from helpers import humansize


STATUSOK = 0            # evaluation successful
ERRORPARSE = 1          # failed to read command
ERRORUNKNOWN = 2        # unknown command
ERRORARGS = 3           # wrong number or wrong type of args
ERROREVAL = 4           # evaluation did not succeed,
                        # because called function failed

STATUSEXIT = 100        # tell calling instance to close comm/pipe/whatever
STATUSDISCONNECT = 101  # tell calling instance to close comm/pipe/whatever


class EvalCmd:
    """ Evaluate commands reveived via RFCOMM or pipe"""

    def __init__(self, parent):
        """ Set in/out fifos to None"""

        self.parent = parent

        self.fifoin = -1
        self.cmdout = None

        # end __init__() #

    def open_fifo(self):
        """ Open input cmd pipe and output"""

        if self.parent.settings.fifoin is not None:
            # Generate/open input fifo.
            if not os.path.exists(self.parent.settings.fifoin):
                os.mkfifo(self.parent.settings.fifoin, 0o666)

            self.parent.log.write(log.MESSAGE, "Opening cmd fifo %s..." %
                                  self.parent.settings.fifoin)
            self.fifoin = os.open(self.parent.settings.fifoin,
                                  os.O_RDONLY | os.O_NONBLOCK)

        if self.parent.settings.cmdout is not None:
            # Open cmd out file for debug.
            self.parent.log.write(log.MESSAGE, "Opening output file %s..." %
                                  self.parent.settings.cmdout)
            self.cmdout = codecs.open(self.parent.settings.cmdout,
                                      "w", "utf-8")

        # end open_fifo() #

    def read_fifo(self):
        """ Check if new command in pipe found and evaluate it

        Called by main daemon loop at each poll.
        """

        if self.fifoin == -1:
            return

        cmd = None
        try:
            cmd = os.read(self.fifoin, 1024)
        except OSError:
            pass

        if cmd:
            self.evalcmd(cmd, 'fifo')

        # end read_fifo() #

    def write_log_file(self, cmd, status, code, msg, res_list):
        """ Write result of evalcmd() to log file if exists"""

        if self.cmdout is None:
            return

        self.cmdout.write(">>> %s\n" % cmd)
        self.cmdout.write("%d %d %d %s\n" % (status, code, len(res_list), msg))
        for line in res_list:
            send_line = u'{0:02d}'.format(len(line))
            for item in line:
                send_line += u'{0:03d}'.format(len(item))+item
            send_msg = u'{0:04d}'.format(len(send_line)) + send_line
            self.cmdout.write(send_msg+'\n')
        self.cmdout.flush()

        # end write_log_file() #

    def evalcmd(self, cmdline, src='Unknown', payload=None):
        """Evaluate command and perform action

        Called by read_fifo() and RFCommServer.

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

        self.parent.log.write(log.MESSAGE,
                              "Eval cmd [%s]: %s; payload size: %d" %
                              (src, " || ".join(line), len(payload)))

        # Command evaluation, starting with 'help', then in alphabetical order.

        # # # # help # # # #

        if cmd == "help":

            ret_list = [
                ['disconnect',
                 '    close bluetooth socket'],
                [''],
                ['getplaystatus',
                 '    show current play status'],
                [''],
                ['hasdevice <storid>',
                 '    1 if device is attached'],
                [''],
                ['lsalldirs <storid>',
                 '    list of all directories on device'],
                [''],
                ['lsdirs <storid> <dirid>',
                 '    list all subdirs in dir'],
                [''],
                ['lsfiles <storid> <dirid>'
                 '    list all files in dir'],
                [''],
                ['keepalive',
                 '    reset disconnect poll count (noop)'],
                [''],
                ['plappendmultiple <mode>',
                 '    receive append instructions (BLUETOOTH only)'],
                [''],
                ['playpause',
                 '    start playing now'],
                [''],
                ['playstatus',
                 '    get status of player'],
                [''],
                ['plclear',
                 '    clear current playlist and start up new one'],
                [''],
                ['plsave',
                 '    save to selected playlist'],
                [''],
                ['plsaveas <name> <creator>',
                 '    save as new playlist'],
                [''],
                ['plsaveasexisting <id>',
                 '    overwrite existsing playlist'],
                [''],
                ['plshow <id> <start> <max> <format>',
                 '    show playlist with id #id from position <start>, '
                 'max <max> items with format <format>'],
                [''],
                ['quit',
                 '    exit program'],
                [''],
                ['plshowlists',
                 '    show all playlists'],
                [''],
                ['poweroff',
                 '    exit application and tell init script to shutdown '
                 'Pi'],
                ['rescan <storid>',
                 '    force rescan of usb device'],
                [''],
                ['setalias <storid> <alias>',
                 '    set alias name for usb device'],
                [''],
                ['showdevices',
                 '    list of connected devices']
            ]

        # # # # disconnect # # # #

        elif cmd == "disconnect":
            ret_stat = STATUSDISCONNECT

        # # # # hasdevice <storid> # # # #

        elif cmd == "hasdevice":
            if len(line) != 2 or int_args[1] is None:
                ret_stat = ERRORARGS
                ret_msg = "hasdevice needs 1 arg"
            else:
                ret_list.append(["%d" %
                                 self.parent.usb.is_connected(int_args[1])])

        # # # # lsalldirs <storid> # # # #

        elif cmd == "lsalldirs":
            if len(line) != 2 or int_args[1] is None:
                ret_stat = ERRORARGS
                ret_msg = "lsalldirs needs 1 arg"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg = "illegal storage id"
                else:
                    ret_list = stor.list_all_dirs

        # # # # lsdirs <storid> <dirid> # # # #

        elif cmd == "lsdirs":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg = "lsalldirs needs 2 args"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg = "illegal storage id"
                else:
                    ret_list = stor.list_dirs(int_args[2])
                    ret_code = LS_DIRS

        # # # # lsfiles <storid> <dirid> # # # #

        elif cmd == "lsfiles":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg = "lsfiles needs 2 args"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg = "illegal storage id"
                else:
                    ret_list = stor.list_files(int_args[2])
                    ret_code = LS_FILES

        # # # # lsfulldir <storid> <dirid> # # # #

        elif cmd == "lsfulldir":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg = "lsfulldir needs 2 args"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg = "illegal storage id"
                else:
                    ret_list = stor.list_full_dir(int_args[2])
                    ret_code = LS_FULL_DIR

        # # # # keepalive # # # #

        elif cmd == "keepalive":
            # nothing to do, timeout poll count will be reset
            # in RFCommServer.read_command()
            ret_msg = "OK"

        # # # # plappendmultiple # # # #

        elif cmd == "plappendmultiple":
            if len(line) != 2 or int_args[1] is None:
                ret_stat = ERRORARGS
                ret_msg = "plappendmultiple needs 2 args"
            elif src != 'rfcomm':
                ret_stat = ERROREVAL
                ret_msg = "plappendmultiple need to be called via BT"
            else:
                added = self.parent.listmngr.append_multiple(payload,
                                                             int_args[1])
                ret_msg = "%d items appended to playlist" % added
                ret_code = PL_ADD_OK

        # # # # playnext # # # #

        elif cmd == "playnext":

            self.parent.play.play_next()
            self.parent.play.send_track_info()
            ret_code = PLAY_NEXT

        # # # # playpause # # # #

        elif cmd == "playpause":
            # pause / unpause or start playing at current playlist pos

            self.parent.play.play_pause()
            self.parent.play.send_track_info()
            ret_code = PLAY_PAUSE

        # # # # playprev # # # #

        elif cmd == "playprev":

            self.parent.play.play_prev()
            self.parent.play.send_track_info()
            ret_code = PLAY_PREV

        # # # # playstatus # # # #

        elif cmd == "playstatus":
            # show current playlist item

            info = self.parent.play.get_play_status()
            if info is None:
                ret_stat = -1
            else:
                ret_list = [info]
            ret_code = PLAY_INFO

        # # # # plclear # # # #

        elif cmd == "plclear":
            if len(line) == 2 and int_args[1] is not None:
                self.parent.listmngr.clear(int_args[1])
            else:
                self.parent.listmngr.clear()
            ret_msg = "Playlist cleared."

        # # # # plgoto # # # #

        elif cmd == "plgoto":
            if len(line) == 3 and int_args[1] is not None and \
                    int_args[2] is not None:
                self.parent.play.load(int_args[1], int_args[2])
                ret_code = PL_JUMP_OK
                self.parent.play.send_track_info()
            elif len(line) == 2 and int_args[1] is not None:
                self.parent.play.load(-1, int_args[1])
                ret_code = PL_JUMP_OK
                self.parent.play.send_track_info()

        # # # #  plmodify # # # #

        elif cmd == "plmodify":
            if len(line) == 2 and int_args[1] is not None:
                self.parent.listmngr.modify_playlist(payload, int_args[1])
                ret_msg = "OK"
                ret_code = PL_MODIFIED
            else:
                ret_stat = ERRORARGS
                ret_msg = "plmodify needs 1 int arg!"

        # # # # plsave # # # #

        elif cmd == "plsave":
            if not self.parent.listmngr.save():
                ret_stat = ERROREVAL
                ret_msg = "Save failed -- name exists or playlist empty!"
            else:
                ret_msg = "Playlist saved."

        # # # # plsaveas # # # #

        elif cmd == "plsaveas":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg = "plsaveas needs 2 args!"
            else:
                if not self.parent.listmngr.save_as(line[1], line[2]):
                    ret_stat = ERROREVAL
                    ret_msg = "Save failed -- name exists or playlist empty!"
                else:
                    ret_msg = "Playlist saved as %s." % line[1]

        # # # # plsaveasexisting # # # #

        elif cmd == "plsaveasexisting":
            if len(line) != 2 or int_args[1] is None:
                ret_stat = ERRORARGS
                ret_msg = "plsaveasexisting needs 1 arg!"
            else:
                if not self.parent.listmngr.save_overwrite(int_args[1]):
                    ret_stat = ERROREVAL
                    ret_msg = \
                        "Save failed -- no such playlist or playlist empty!"
                else:
                    ret_msg = "Playlist %d overwitten." % int_args[1]

        # # # # plshow # # # #

        elif cmd == "plshow":
            if len(line) != 5 or int_args[1] is None or \
                    int_args[2] is None or int_args[3] is None or \
                    int_args[4] is None:
                ret_stat = ERRORARGS
                ret_msg = "plshow needs 4 args"
            else:
                ret_list = self.parent.listmngr.list_playlist(
                    list_id=int_args[1],
                    start_at=int_args[2],
                    max_items=int_args[3],
                    printformat=line[4])
                ret_msg = "OK"
                ret_code = PL_SHOW

        # # # # plshow # # # #

        elif cmd == "plshowlists":
            ret_list = self.parent.listmngr.list_playlists()

        # # # # poweroff # # # #

        elif cmd == "poweroff":
            ret_stat = STATUSEXIT
            self.parent.keep_run = 0
            self.parent.ret_code = 10  # tell init script to invoke poweroff

        # # # # quit # # # #

        elif cmd == "quit":
            ret_stat = STATUSEXIT
            self.parent.keep_run = 0

        # # # # rescan # # # #

        elif cmd == "rescan":
            if len(line) != 2:
                ret_stat = ERRORARGS
                ret_msg = "rescan needs 1 arg"
            else:
                if not self.parent.usb.rescan_usb_stor(int_args[1]):
                    ret_stat = ERROREVAL
                    ret_msg = "device not rescaned (no such device?)"
                else:
                    ret_msg = "device %d rescaned." % int_args[1]

        # # # # search # # # #

        elif cmd == "search":
            if len(line) < 4:
                ret_stat = ERRORARGS
                ret_msg = "search needs 3+ args"
            elif int_args[1] is None or int_args[2] is None:
                ret_stat = ERRORARGS
                ret_msg = "Usage: search MODE LIMIT PATTERN"
            else:
                pattern = ' '.join(line[3:])
                ret_list = self.parent.usb.search_files(pattern, int_args[1],
                                                        int_args[2])
                ret_code = SEARCH_RES

        # # # # setalias # # # #

        elif cmd == "setalias":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg = "rescan needs 2 args"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg = "illegal storage id"
                else:
                    if not stor.update_alias(line[2]):
                        ret_stat = ERROREVAL
                        ret_msg = "alias exists in database"
                    else:
                        ret_msg = "Alias set to %s for device %d" % \
                            (line[2], int_args[1])

        # # # # showdevices # # # #

        elif cmd == "showdevices":
            for dev in self.parent.usb.usbdevs:
                # TODO: bytes used, bytes free
                ret_list.append(['%d' % dev.storid,
                                 '%s' % dev.uuid,
                                 u'%s' % dev.alias,
                                 '%d' % dev.revision,
                                 '%d' % dev.totsubdirs,
                                 '%d' % dev.totfiles,
                                 humansize(dev.bytes_free),
                                 humansize(dev.cur_tot_bytes)
                                 ])
            if not ret_list:
                ret_list = [["-1 NONE"]]
            ret_code = SHOW_DEVICES

        # # # # vol_dec / vol_inc # # # #

        elif cmd == "voldec" or cmd == "volinc":
            vol_change = self.parent.settings.default_vol_change

            if len(line) == 2 and int_args[1] is not None:
                vol_change = int_args[1]

            if cmd == "voldec":
                self.parent.play.vol_dec(vol_change)
            else:
                self.parent.play.vol_inc(vol_change)

            # let APP set correct volume slider position
            self.parent.play.send_track_info()

        # # # # vol_set # # # #

        elif cmd == "volset":
            if len(line) != 2:
                ret_stat = ERRORARGS
                ret_msg = "volset needs 1 arg"
            else:
                if int_args[1] is None:
                    ret_stat = ERRORARGS
                    ret_msg = "volsset needs int arg"
                else:
                    self.parent.play.vol_set(int_args[1])
                    # let APP set correct volume slider position
                    self.parent.play.send_track_info()

        else:
            ret_stat = ERRORUNKNOWN
            ret_msg = "unknown command"

        self.write_log_file(cmd, ret_stat, ret_code, ret_msg, ret_list)

        self.parent.log.write(log.MESSAGE, ">>> %s" % ret_msg)

        if src != 'button':
            if ret_stat == STATUSOK:
                self.parent.led.flash_led(led.LED_WHITE, 1.0)
            else:
                self.parent.led.flash_led(led.LED_RED, 1.0)

        return [ret_stat, ret_code, ret_msg, ret_list]

        # end evalcmd() #
