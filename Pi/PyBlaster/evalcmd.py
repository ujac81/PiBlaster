"""evalcmd.py -- Evaluate commands reveived via RFCOMM or pipe

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import codecs
import fcntl
import os
import sys

import log


STATUSOK      = 0   # evaluation successful
ERRORPARSE    = 1   # failed to read command
ERRORUNKNOWN  = 2   # unknown command
ERRORARGS     = 3   # wrong number or wrong type of args
ERROREVAL     = 4   # evaluation did not succeed,
                    # because called function failed

STATUSEXIT    = 100 # tell calling instance to close comm/pipe/whatever



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
      self.cmdout = codecs.open(self.parent.settings.cmdout, "w", "utf-8")

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

  def evalcmd(self, cmd, src='Unknonw'):
    """Evaluate command and perform action

    Called by read_fifo() and RFCommServer.

    return [status, status_msg, result_list]
    """
    cmd = cmd.strip()

    ret_stat = STATUSOK
    ret_msg  = "OK"
    ret_list = []

    self.parent.log.write(log.MESSAGE, "Eval cmd [%s]: %s" % (src,cmd))

    # Command evaluation, starting with 'help', then in alphabetical order.

    # # # # help # # # #

    if cmd.startswith("help"):

      ret_list = [
        'lsalldirs <storid>           -- list of all directories on device',
        'lsdirs <storid> <dirid>      -- list all subdirs in dir',
        'lsfiles <storid> <dirid>     -- list all files in dir',
        'keepalive                    -- reset disconnect poll count (noop)',
        'quit                         -- exit program',
        'rescan <storid>              -- force rescan of usb device',
        'showdevices                  -- list of connected devices'
        ]

    # # # # lsalldirs <storid> # # # #

    elif cmd.startswith("lsalldirs"):
      line = cmd.split()
      if len(line) != 2:
        ret_stat = ERRORARGS
        ret_msg  = "lsalldirs needs 1 arg"
      else:
        stor = self.parent.usb.get_dev_by_strid(line[1])
        if not stor:
          ret_stat = ERRORARGS
          ret_msg  = "illegal storage id"
        else:
          ret_list = stor.list_all_dirs()


    # # # # lsdirs <storid> <dirid> # # # #

    elif cmd.startswith("lsdirs"):
      line = cmd.split()
      if len(line) != 3:
        ret_stat = ERRORARGS
        ret_msg  = "lsalldirs needs 2 args"
      else:
        stor = self.parent.usb.get_dev_by_strid(line[1])
        if not stor:
          ret_stat = ERRORARGS
          ret_msg  = "illegal storage id"
        else:
          ret_list = stor.list_dirs(line[2])

    # # # # lsfiles <storid> <dirid> # # # #

    elif cmd.startswith("lsfiles"):
      line = cmd.split()
      if len(line) != 3:
        ret_stat = ERRORARGS
        ret_msg  = "lsfiles needs 2 args"
      else:
        stor = self.parent.usb.get_dev_by_strid(line[1])
        if not stor:
          ret_stat = ERRORARGS
          ret_msg  = "illegal storage id"
        else:
          ret_list = stor.list_files(line[2])

    # # # # keepalive # # # #

    elif cmd == "keepalive":
      # nothing to do, timeout poll count will be reset
      # in RFCommServer.read_command()
      ret_msg = "OK"

    # # # # quit # # # #

    elif cmd == "quit":
      ret_stat = STATUSEXIT
      self.parent.keep_run = 0

    # # # # rescan # # # #

    elif cmd.startswith("rescan"):
      line = cmd.split()
      if len(line) != 2:
        ret_stat = ERRORARGS
        ret_msg  = "rescan needs 1 arg"
      else:
        if not self.parent.usb.rescan_usb_stor(line[1]):
          ret_stat = ERROREVAL
          ret_msg  = "device not rescaned (no such device?)"

    # # # # showdevices # # # #

    elif cmd == "showdevices":
      for dev in self.parent.usb.usbdevs:
        ret_list.append("||%d||%s||" % (dev.storid, dev.label))
      if not ret_list: ret_list = ["-1 NONE"]

    else:
      ret_stat = ERRORUNKNOWN
      ret_msg  = "unknown command"

    self.write_log_file(cmd, ret_stat, ret_msg, ret_list)
    return [ret_stat, ret_msg, ret_list]

    # end evalcmd() #
