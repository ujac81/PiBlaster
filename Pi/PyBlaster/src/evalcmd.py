"""evalcmd.py -- Evaluate commands reveived via RFCOMM or pipe

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import codecs
import fcntl
import os
import re
import sys

import log
from helpers import humansize


STATUSOK            = 0     # evaluation successful
ERRORPARSE          = 1     # failed to read command
ERRORUNKNOWN        = 2     # unknown command
ERRORARGS           = 3     # wrong number or wrong type of args
ERROREVAL           = 4     # evaluation did not succeed,
                            # because called function failed

STATUSEXIT          = 100   # tell calling instance to close comm/pipe/whatever
STATUSDISCONNECT    = 101   # tell calling instance to close comm/pipe/whatever



class EvalCmd:
    """ Evaluate commands reveived via RFCOMM or pipe"""

    def __init__(self, parent):
        """ Set in/out fifos to None"""

        self.parent = parent

        self.fifoin = None
        self.cmdout = None

        # end __init__() #

    def open_fifo(self):
        """ Open input cmd pipe and output"""

        if self.parent.settings.fifoin is not None:
            # Generate/open input fifo.
            if not os.path.exists(self.parent.settings.fifoin):
                os.mkfifo(self.parent.settings.fifoin, 0666)

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

        if self.fifoin is None:
            return

        cmd = None
        try:
            cmd = os.read(self.fifoin, 1024)
        except:
            pass

        if cmd:
            self.evalcmd(cmd, 'fifo')

        # end read_fifo() #

    def write_log_file(self, cmd, status, msg, res_list):
        """ Write result of evalcmd() to log file if exists"""

        if self.cmdout is None:
            return

        self.cmdout.write(">>> %s\n" % cmd)
        self.cmdout.write("%d\n" % status)
        self.cmdout.write("%s\n" % msg)
        self.cmdout.write("%d\n" % len(res_list))
        for line in res_list:
            self.cmdout.write(u'%s\n' % line)

        self.cmdout.flush()

        # end write_log_file() #

    def evalcmd(self, cmdline, src='Unknonw'):
        """Evaluate command and perform action

        Called by read_fifo() and RFCommServer.

        return [status, code, status_msg, result_list]
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
        ret_msg  = "OK"
        ret_code = -1
        ret_list = []

        self.parent.log.write(log.MESSAGE, "Eval cmd [%s]: %s" %
                              (src, " || ".join(line)))

        # Command evaluation, starting with 'help', then in alphabetical order.

        # # # # help # # # #

        if cmd == "help":

            ret_list = [
                'disconnect',
                '    close bluetooth socket',
                '',
                'hasdevice <storid>',
                '    1 if device is attached',
                '',
                'lsalldirs <storid>',
                '    list of all directories on device',
                '',
                'lsdirs <storid> <dirid>',
                '    list all subdirs in dir',
                '',
                'lsfiles <storid> <dirid>'
                '    list all files in dir',
                '',
                'keepalive',
                '    reset disconnect poll count (noop)',
                '',
                'plappenddir <mode> <storid> <dirid>',
                '    append directory to playlist',
                '',
                'plappendfile <mode> <storid> <dirid> <fileid>',
                '    append directory to playlist',
                '',
                'plappendmultiple <mode> <num_rows>',
                '    receive num_rows append instructions (BLUETOOTH only)'
                '',
                'plclear',
                '    clear current playlist and start up new one',
                '',
                'plsave',
                '    save to selected playlist',
                '',
                'plsaveas <name> <creator>',
                '    save as new playlist',
                '',
                'plsaveasexisting <id>',
                '    overwrite existsing playlist',
                '',
                'plshow <id> <start> <max> <format>',
                '    show playlist with id #id from position <start>, '\
                        'max <max> items with format <format>',
                '',
                'quit',
                '    exit program',
                '',
                'plshowlists',
                '    show all playlists',
                '',
                'rescan <storid>',
                '    force rescan of usb device',
                '',
                'setalias <storid> <alias>',
                '    set alias name for usb device',
                '',
                'showdevices',
                '    list of connected devices'
                ]

        # # # # disconnect # # # #

        elif cmd == "disconnect":
            ret_stat = STATUSDISCONNECT

        # # # # hasdevice <storid> # # # #

        elif cmd == "hasdevice":
            if len(line) != 2 or int_args[1] is None:
                ret_stat = ERRORARGS
                ret_msg    = "hasdevice needs 1 arg"
            else:
                ret_list.append("%d" %
                                self.parent.usb.is_connected(int_args[1]))

        # # # # lsalldirs <storid> # # # #

        elif cmd == "lsalldirs":
            if len(line) != 2 or int_args[1] is None:
                ret_stat = ERRORARGS
                ret_msg  = "lsalldirs needs 1 arg"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg  = "illegal storage id"
                else:
                    ret_list = stor.list_all_dirs()


        # # # # lsdirs <storid> <dirid> # # # #

        elif cmd == "lsdirs":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg  = "lsalldirs needs 2 args"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg  = "illegal storage id"
                else:
                    ret_list = stor.list_dirs(int_args[2])
                    ret_code = 102

        # # # # lsfiles <storid> <dirid> # # # #

        elif cmd == "lsfiles":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg    = "lsfiles needs 2 args"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg    = "illegal storage id"
                else:
                    ret_list = stor.list_files(int_args[2])
                    ret_code = 103

        # # # # keepalive # # # #

        elif cmd == "keepalive":
            # nothing to do, timeout poll count will be reset
            # in RFCommServer.read_command()
            ret_msg = "OK"

        # # # # plappenddir # # # #

        elif cmd == "plappenddir":
            if len(line) != 3 or int_args[1] is None or int_args[2] is None:
                ret_stat = ERRORARGS
                ret_msg  = "plappenddir needs 3 args"
            else:
                num_ins = self.parent.listmngr.insert_dir(
                    ids=[int_args[1], int_args[2]])
                ret_list=[num_ins]
                ret_msg = "%d items appended to playlist" % num_ins

        # # # # plappendmultiple # # # #

        elif cmd == "plappendmultiple":
            if len(line) != 3 or int_args[1] is None or int_args[2] is None:
                ret_stat = ERRORARGS
                ret_msg  = "plappendmultiple needs 3 args"
            elif src != 'rfcomm':
                ret_stat = ERROREVAL
                ret_msg  = "plappendmultiple need to be called via BT"
            else:
                rows = self.parent.rfcomm.read_rows(int_args[2])

                if len(rows) == 0:
                    # we got BT error
                    ret_list=[]
                    ret_msg = "COMM ERROR"
                else:
                    ret_list=[]
                    ret_msg = "%d items appended to playlist" % len(rows)

        # # # # plclear # # # #

        elif cmd == "plclear":
            self.parent.listmngr.clear()
            ret_msg = "Playlist cleared."

        # # # # plsave # # # #

        elif cmd == "plsave":
            if not self.parent.listmngr.save():
                ret_stat = ERROREVAL
                ret_msg  = "Save failed -- name exists or playlist empty!"
            else:
                ret_msg  = "Playlist saved."

        # # # # plsaveas # # # #

        elif cmd == "plsaveas":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg  = "plsaveas needs 2 args!"
            else:
                if not self.parent.listmngr.save_as(line[1], line[2]):
                    ret_stat = ERROREVAL
                    ret_msg  = "Save failed -- name exists or playlist empty!"
                else:
                    ret_msg  = "Playlist saved as %s." % line[1]

        # # # # plsaveasexisting # # # #

        elif cmd == "plsaveasexisting":
            if len(line) != 2 or int_args[1] is None:
                ret_stat = ERRORARGS
                ret_msg  = "plsaveasexisting needs 1 arg!"
            else:
                if not self.parent.listmngr.save_overwrite(int_args[1]):
                    ret_stat = ERROREVAL
                    ret_msg  = \
                        "Save failed -- no such playlist or playlist empty!"
                else:
                    ret_msg  = "Playlist %d overwitten." % int_args[1]

        # # # # plshow # # # #

        elif cmd == "plshow":
            if len(line) != 5 or int_args[1] is None or \
                    int_args[2] is None or int_args[3] is None:
                ret_stat = ERRORARGS
                ret_msg  = "plshow needs 4 args"
            else:
                ret_list = self.parent.listmngr.list_playlist(
                    playlist=int_args[1],
                    start_at=int_args[2],
                    max_items=int_args[3],
                    printformat=line[4])

        # # # # plshow # # # #

        elif cmd == "plshowlists":
            ret_list = self.parent.listmngr.list_playlists()

        # # # # quit # # # #

        elif cmd == "quit":
            ret_stat = STATUSEXIT
            self.parent.keep_run = 0

        # # # # rescan # # # #

        elif cmd == "rescan":
            if len(line) != 2:
                ret_stat = ERRORARGS
                ret_msg  = "rescan needs 1 arg"
            else:
                if not self.parent.usb.rescan_usb_stor(int_args[1]):
                    ret_stat = ERROREVAL
                    ret_msg  = "device not rescaned (no such device?)"
                else:
                    ret_msg  = "device %d rescaned." % int_args[1]

        # # # # setalias # # # #

        elif cmd == "setalias":
            if len(line) != 3:
                ret_stat = ERRORARGS
                ret_msg  = "rescan needs 2 args"
            else:
                stor = self.parent.usb.get_dev_by_storid(int_args[1])
                if stor is None:
                    ret_stat = ERRORARGS
                    ret_msg  = "illegal storage id"
                else:
                    if not stor.update_alias(line[2]):
                        ret_stat = ERROREVAL
                        ret_msg  = "alias exists in database"
                    else:
                        ret_msg  = "Alias set to %s for device %d" % \
                            (line[2], int_args[1])

        # # # # showdevices # # # #

        elif cmd == "showdevices":
            for dev in self.parent.usb.usbdevs:
                # TODO: bytes used, bytes free
                ret_list.append("||%d||%s||%s||%d||%d||%d||%s||%s||" %
                                (dev.storid, dev.uuid, dev.alias, dev.revision,
                                dev.totsubdirs, dev.totfiles,
                                humansize(dev.bytes_free),
                                humansize(dev.cur_tot_bytes)))
            if not ret_list: ret_list = ["-1 NONE"]
            ret_code = 101

        else:
            ret_stat = ERRORUNKNOWN
            ret_msg  = "unknown command"

        self.write_log_file(cmd, ret_stat, ret_msg, ret_list)

        self.parent.log.write(log.MESSAGE, ">>> %s" % ret_msg)
        return [ret_stat, ret_code, ret_msg, ret_list]

        # end evalcmd() #
