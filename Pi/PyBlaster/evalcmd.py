"""Evaluate commands reveived via RFCOMM or pipe
"""

STATUSOK      = 0
ERRORPARSE    = 1
ERRORUNKNOWN  = 2
ERRORARGS     = 3

STATUSEXIT    = 100 # tell calling instance to close comm/pipe/whatever



class EvalCmd:
  """
  """
  def __init__(self, parent):
    """
    """
    self.parent = parent


  def evalcmd(self, cmd):
    """

      return [status, status_msg, result_list]
    """
    ret_stat = STATUSOK
    ret_msg  = "OK"
    ret_list = []

    self.parent.log.write(log.MESSAGE, "Eval cmd: %s" % cmd)

    if cmd.startswith("lsalldirs"):
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

    elif cmd == "keepalive":
      ret_msg = "OK" # nothing to do, timeout poll count will be reset in RFCommServer.read_command()

    elif cmd == "quit":
      ret_stat = STATUSEXIT

    elif cmd == "showdevices":
      for dev in self.parent.usb.usbdevs:
        ret_list.append("%d %s" % (dev.storid, dev.label))
      if not len(ret_list): ret_list = ["-1 NONE"]

    else:
      ret_stat = ERRORUNKNOWN
      ret_msg  = "unknown command"

    return [ret_stat, ret_msg, ret_list]

    # enf evalcmd() #
