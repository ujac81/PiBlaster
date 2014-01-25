"""rfcommserver.py -- Send/recv commands/results via bluetooth channel

To enable visible server do
 $ sudo hciconfig hci0 piscan

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import bluetooth

import log
import evalcmd


NOTCONNECTED    = 0
CONNECTED       = 1
AUTHORIZED      = 2

class RFCommServer:
    """Send/recv commands/results via bluetooth channel"""

    def __init__(self, parent):
        """Set state to not connected"""

        self.parent         = parent
        self.mode           = NOTCONNECTED
        self.client_sock    = None
        self.client_info    = None
        self.timeout        = 1     # socket timeouts for non blocking con.
        self.timeoutpolls   = 500   # disconnect after N inactivity timeouts
        self.nowpolls       = 0     # reset after each receive,
                                    # incremented while waiting for data
        self.cmdbuffer      = []    # split incoming commands by ' !EOL! '


    def start_server(self):
        """Open bluetooth server socket and advertise service"""

        self.parent.led.set_led_blue(1)

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        self.server_sock.bind(( "", bluetooth.PORT_ANY ))
        self.server_sock.listen( 1 ) # max conns
        self.port = self.server_sock.getsockname()[1]
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        bluetooth.advertise_service(self.server_sock, "PyBlaster",
                                    service_id=self.uuid,
                                    service_classes=
                                        [self.uuid,
                                         bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                    )

        self.server_sock.settimeout(self.timeout)
        self.parent.log.write(log.MESSAGE,
                              "RFCOMM service opened as PyBlaster")
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
                                      (self.client_info[0],
                                       self.client_info[1]))
                self.mode = CONNECTED
                self.client_sock.settimeout(self.timeout)
                self.parent.led.set_led_blue(1)
                self.nowpolls = 0
                self.cmdbuffer = []

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
                self.nowpolls = 0

                if self.mode == CONNECTED:
                    # check authorization
                    if data == "1234":
                        self.mode = AUTHORIZED
                        self.parent.log.write(log.MESSAGE,
                                              "Authorized connection.")
                        self.send_client(0, "Password OK", ["accepted."])
                    else:
                        self.send_client(1, "Wrong password", ["rejected."])
                        self.disconnect()

                elif self.mode == AUTHORIZED:
                    # split command
                    self.split_cmd_to_buffer(data)

                # if data #

            # if CONNECTED or AUTHORIZED #

        if self.mode == AUTHORIZED:
            # dry run buffer if connected
            while len(self.cmdbuffer):
                self.read_command(self.cmdbuffer.pop(0))

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

    def send_client(self, status, msg, message_list):
        """Send data package

            - result code from evalcmd
            - confirm message
            - list of message lines
        """

        # TODO timeout mechanism
        self.parent.log.write(log.DEBUG1, "DEBUG send: %d || %s || %d" %
                              (status, msg, len(message_list)))
        self.client_sock.send(str(status) + ' !EOL! ')
        self.client_sock.send(msg + ' !EOL! ')
        self.client_sock.send(str(len(message_list)) + ' !EOL! ')
        for line in message_list:
            self.client_sock.send(line.encode('utf-8') + ' !EOL! ')


        # end send_client() #

    def split_cmd_to_buffer(self, cmd):
        """Split incoming commands with !EOL! """
        rows = cmd.split(' !EOL! ')
        for i in rows:
            add = i.strip()
            if add != '':
                self.parent.log.write(log.DEBUG1, "DEBUG recv: %s" % add)
                self.cmdbuffer.append(add)

    def read_command(self, cmd):
        """Evalute command received from client socket if AUTHORIZED."""

        self.nowpolls = 0

        status, msg, res_list = self.parent.cmd.evalcmd(cmd, 'rfcomm')
        self.send_client(status, msg, res_list)

        if status == evalcmd.STATUSEXIT or status == evalcmd.STATUSDISCONNECT:
            self.parent.log.write(log.MESSAGE, "Got disconnect command.")
            self.disconnect()

        # end read_command() #

    def read_rows(self, count):
        """Read multiple rows from bluetooth socket.

            return rows as list or empty list on BT error
        """

        result = []

        while 1:
            if len(result) == count:
                break

            data = None
            try:
                data = self.client_sock.recv(1024)
            except bluetooth.btcommon.BluetoothError:
                return []

            self.split_cmd_to_buffer(data)

            while len(self.cmdbuffer):
                if len(result) == count:
                    break
                result.append(self.cmdbuffer.pop(0))

        return result

        # end read_rows() #


