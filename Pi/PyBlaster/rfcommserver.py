"""rfcommserver.py -- Send/recv commands/results via bluetooth channel

To enable visible server do
 $ sudo hciconfig hci0 piscan

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import bluetooth

import log
import evalcmd


NOTCONNECTED  = 0
CONNECTED     = 1
AUTHORIZED    = 2

class RFCommServer:
  """Send/recv commands/results via bluetooth channel"""

  def __init__(self, parent):
    """Set state to not connected"""

    self.parent       = parent
    self.mode         = NOTCONNECTED
    self.client_sock  = None
    self.client_info  = None
    self.timeout      = 0.01  # socket timeouts for non blocking connection
    self.timeoutpolls = 1000  # disconnect after N inactivity timeouts
    self.nowpolls     = 0     # reset after each receive,
                              # incremented while waiting for data

  def start_server(self):
    """Open bluetooth server socket and advertise service"""

    self.parent.led.set_led_blue(1)

    self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    self.server_sock.bind(( "", bluetooth.PORT_ANY ))
    self.server_sock.listen( 1 ) # max conns
    self.port = self.server_sock.getsockname()[1]
    self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    bluetooth.advertise_service( self.server_sock, "PyBlaster",
                                 service_id = self.uuid,
                                 service_classes =
                                 [ self.uuid, bluetooth.SERIAL_PORT_CLASS ],
                                 profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
                                )

    self.server_sock.settimeout(self.timeout)
    self.parent.log.write(log.MESSAGE, "RFCOMM service opened as PyBlaster")
    self.parent.led.set_led_blue(0)
    self.mode = NOTCONNECTED

    # end start_server() #

  def read_socket(self):
    """Check if command found in socket

    Called by main daemon loop at every poll.
    """

    if self.mode == NOTCONNECTED:

      try:
        self.client_sock, self.client_info = self.server_sock.accept()
      except bluetooth.btcommon.BluetoothError:
        self.client_sock = None
        self.client_info = None
        pass

      if self.client_sock:
        self.parent.log.write(log.MESSAGE,
                              "Got connection from %s on channel %d" %
                              ( self.client_info[0], self.client_info[1] ))
        self.mode = CONNECTED
        self.client_sock.settimeout(self.timeout)
        self.parent.led.set_led_blue(1)
        self.nowpolls = 0

      # if NOTCONNECTED #

    if self.mode == CONNECTED or self.mode == AUTHORIZED:

      data = None
      try:
        data = self.client_sock.recv(1024)
      except bluetooth.btcommon.BluetoothError:
        pass

      self.nowpolls += 1
      if self.nowpolls > self.timeoutpolls:
        self.parent.log.write(log.MESSAGE, "Connection timed out")
        self.disconnect()

      if self.nowpolls % 500 == 0:
        self.parent.log.write(log.DEBUG1,
                              "Timeout poll count %d" % self.nowpolls)

      if data:
        self.parent.log.write(log.DEBUG1, "DEBUG recv: %s" % data)

        self.nowpolls = 0

        if self.mode == CONNECTED:
          # check authorization
          if data == "1234":
            self.mode = AUTHORIZED
            self.parent.log.write(log.MESSAGE, "Authorized connection.")
            self.send_client(["accepted."])
          else:
            self.disconnect()

        elif self.mode == AUTHORIZED:
          # parse command
          self.read_command(data)

        # if data #

      # if CONNECTED or AUTHORIZED #

    # end read_socket() #


  def disconnect(self):
    """Close sockets and restart server

    Called after timeout poll count reached or if connection closed by
    wrong password or on purpose.
    """

    self.server_sock.close()
    self.client_sock.close()
    self.parent.log.write(log.MESSAGE, "Closed connection.")
    self.start_server()

  def send_client(self, status, msg, res_list):
    """Send data package

      - result code from evalcmd
      - confirm message
      - number of result lines
      - lines
      - lines
      ...
      - lines
    """

    # TODO timeout mechanism
    self.client_sock.send(str(status))
    self.client_sock.send(msg)
    self.client_sock.send(str(len(message_list)))
    for line in message_list:
      self.client_sock.send(line)

    # end send_client() #

  def read_command(self, cmd):
    """Evalute command received from client socket if AUTHORIZED."""

    self.nowpolls = 0

    status, msg, res_list = self.parent.cmd.evalcmd(cmd, 'rfcomm')
    self.send_client(status, msg, res_list)

    if status == evalcmd.STATUSEXIT:
      self.disconnect()

    # end read_command() #

