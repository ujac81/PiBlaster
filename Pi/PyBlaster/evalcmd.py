"""Evaluate commands reveived via RFCOMM or pipe
"""

import os, fcntl, sys

import log


STATUSOK      = 0
ERRORPARSE    = 1
ERRORUNKNOWN  = 2
ERRORARGS     = 3
ERROREVAL     = 4

STATUSEXIT    = 100 # tell calling instance to close comm/pipe/whatever



class EvalCmd:
  """
  """
  def __init__(self, parent):
    """
    """
    self.parent = parent

    self.fifoin   = None
    self.fifoout  = None
    self.cmdout   = None

    # end __init__() #


  def open_fifo(self):
    """
    """

    if self.parent.settings.fifoin:
      # generate/open input fifo
      if not os.path.exists(self.parent.settings.fifoin):
        os.mkfifo(self.parent.settings.fifoin, 0666)

      self.parent.log.write(log.MESSAGE, "Opening cmd fifo %s..." % self.parent.settings.fifoin)
      self.fifoin = os.open(self.parent.settings.fifoin, os.O_RDONLY | os.O_NONBLOCK)

    if self.parent.settings.fifoout:
      """
      """
      if self.parent.settings.fifoout:
        # open outgoing fifo
        self.parent.log.write(log.MESSAGE, "Opening output stream %s..." % self.parent.settings.fifoout)
        self.fifoout = os.open(self.parent.settings.fifoout, os.O_WRONLY | os.O_CREAT)

    if self.parent.settings.cmdout:
      # open cmd out file for debug
      self.parent.log.write(log.MESSAGE, "Opening output file %s..." % self.parent.settings.cmdout)
      self.cmdout = open(self.parent.settings.cmdout, "a")
    # end open_fifo() #



  def read_fifo(self):
    """
    """
    if not self.fifoin: return

    cmd = None
    try:
      cmd = os.read(self.fifoin, 1024)
    except: pass

    if cmd: self.evalcmd(cmd, 'fifo')

    # end read_fifo() #

  def write_fifo(self, cmd, status, msg, res_list):
    """
    """
    self.write_log_file(cmd, status, msg, res_list)

    if not self.fifoout: return

    os.write(self.fifoout, ">>> %s\n" % cmd)
    os.write(self.fifoout, "%d\n" % status)
    os.write(self.fifoout, "%s\n" % msg)
    os.write(self.fifoout, "%d\n" % len(res_list))
    for line in res_list:
      os.write(self.fifoout, "%s\n" % line)

    os.fsync(self.fifoout)


  def write_log_file(self, cmd, status, msg, res_list):
    """
    """
    if not self.cmdout: return

    self.cmdout.write(">>> %s\n" % cmd)
    self.cmdout.write("%d\n" % status)
    self.cmdout.write("%s\n" % msg)
    self.cmdout.write("%d\n" % len(res_list))
    for line in res_list:
      self.cmdout.write("%s\n" % line)

    self.cmdout.flush()


  def evalcmd(self, cmd, src='Unknonw'):
    """

      return [status, status_msg, result_list]
    """
    cmd = cmd.strip()

    ret_stat = STATUSOK
    ret_msg  = "OK"
    ret_list = []

    self.parent.log.write(log.MESSAGE, "Eval cmd [%s]: %s" % (src,cmd))

    # command evaluation, starting with 'help', then in alphabetical order

    # # # # help # # # #

    if cmd.startswith("help"):

      ret_list.append('lsalldirs <storid>           -- list of all directories on device')
      ret_list.append('lsdirs <storid> <dirid>      -- list all subdirs in dir')
      ret_list.append('lsfiles <storid> <dirid>     -- list all files in dir')
      ret_list.append('keepalive                    -- reset disconnect poll count (noop)')
      ret_list.append('quit                         -- exit program')
      ret_list.append('rescan <storid>              -- force rescan of usb device')
      ret_list.append('showdevices                  -- list of connected devices')

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
      ret_msg = "OK" # nothing to do, timeout poll count will be reset in RFCommServer.read_command()

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
      if not len(ret_list): ret_list = ["-1 NONE"]

    else:
      ret_stat = ERRORUNKNOWN
      ret_msg  = "unknown command"


    self.write_fifo(cmd, ret_stat, ret_msg, ret_list)
    return [ret_stat, ret_msg, ret_list]

    # enf evalcmd() #
