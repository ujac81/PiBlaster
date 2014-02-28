"""rfcommserver.py -- Send/recv commands/results via bluetooth channel

To enable visible server do
 $ sudo hciconfig hci0 piscan

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import bluetooth

from codes import *
import log
import evalcmd


NOTCONNECTED = 0
CONNECTED = 1
AUTHORIZED = 2


class RFCommServer:
    """Send/recv commands/results via bluetooth channel"""

    def __init__(self, parent):
        """Set state to not connected"""

        self.parent = parent
        self.mode = NOTCONNECTED
        self.client_sock = None
        self.client_info = None
        self.timeout = 0.05  # socket timeouts for non blocking con.
        self.comm_timeout = 2  # increase timeout on send/recv
        self.timeoutpolls = 500  # disconnect after N inactivity timeouts
        self.nowpolls = 0  # reset after each receive,
        # incremented while waiting for data
        self.cmdbuffer = []  # split incoming commands by lines
        self.server_sock = None
        self.port = 0
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.next_buffer_size = -1  # set in read_socket to receive lines

    def start_server(self):
        """Open bluetooth server socket and advertise service"""

        self.parent.led.set_led_blue(1)

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)  # max conns
        self.port = self.server_sock.getsockname()[1]

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

            self.receive_into_buffer()

            self.nowpolls += 1
            if self.nowpolls > self.timeoutpolls:
                self.parent.log.write(log.MESSAGE, "Connection timed out")
                self.disconnect()

            if self.nowpolls % 500 == 0:
                self.parent.log.write(log.DEBUG1, "Timeout poll count %d" %
                                                  self.nowpolls)

            # dry run buffer if connected
            while len(self.cmdbuffer):
                self.nowpolls = 0
                self.read_command(self.cmdbuffer.pop(0))

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

    def send_client(self, msg_id, status, code, msg, message_list):
        """Send data package to PiBlaster APP via bluetooth

        :param msg_id: message id as received by read_command
        :param status: status from evalcmd
        :param code: result code to tell PiBlaster APP which data is sent
        :param msg: string message to be displayed at PiBlaster APP
        :param message_list: matrix of payload lines
        """

        self.client_sock.settimeout(self.comm_timeout)
        self.parent.led.set_led_green(1)

        self.parent.log.write(log.DEBUG1,
                              "DEBUG send: %d || %d || %d || %d || %s" %
                              (msg_id, status, code, len(message_list), msg))

        # send msg header
        # 4 ints line length, followed by 'msg_id status code payload_len msg'
        full_msg = u'{0:04d}{1:04d}{2:04d}{3:06d}{4:s}'.\
            format(msg_id, status, code, len(message_list), msg)
        send_msg = u'{0:04d}{1:s}'.format(len(full_msg), full_msg)
        # self.parent.log.write(log.DEBUG3, "--->>> SEND: "+send_msg)
        self.client_sock.send(send_msg)

        if self.recv_ok_byte():
            for line in message_list:
                # TODO handle exception if comm breaks on send
                # construct line by prefixing each field with its length
                send_line = u'{0:04d}{1:02d}'.format(msg_id, len(line))
                for item in line:
                    send_line += u'{0:03d}'.format(len(item))+item
                send_msg = u'{0:04d}'.format(len(send_line)) + send_line
                self.client_sock.send(send_msg.encode('utf-8'))
                if not self.recv_ok_byte():
                    break

        self.client_sock.settimeout(self.timeout)
        self.parent.led.set_led_green(0)

        # end send_client() #

    def read_command(self, cmd):
        """Evaluate command received from client socket if AUTHORIZED."""

        self.nowpolls = 0

        # message id is first field in command, truncate from rest of command
        cmd_split = cmd.split(' ')
        msg_id = -1
        payload_size = -1
        error_cmd = False
        if len(cmd_split) < 3:
            error_cmd = True
        else:
            try:
                msg_id = int(cmd_split[0])
                payload_size = int(cmd_split[1])
            except ValueError:
                msg_id = -1
                payload_size = -1
                error_cmd = True

        if error_cmd:
            self.parent.log.write(log.ERROR,
                                  "[ERROR] Protocol error: %s" % cmd)
            return

        cmd = cmd[len(cmd_split[0]) + len(cmd_split[1]) + 2:]
        payload = self.read_rows(payload_size)

        if self.mode != AUTHORIZED:
            # check if password has been sent
            if cmd == self.parent.settings.pin1:
                self.mode = AUTHORIZED
                self.parent.log.write(log.MESSAGE, "BT AUTHORIZED")
                self.send_client(0, 0, PASS_OK, "Password ok.", [])
            else:
                self.parent.log.write(log.MESSAGE, "BT NOT AUTHORIZED")
                self.send_client(0, 0, PASS_ERROR, "Wrong password.", [])
                self.disconnect()
        elif self.mode == AUTHORIZED:
            status, code, msg, res_list = \
                self.parent.cmd.evalcmd(cmd, 'rfcomm', payload)

            send_failed = False
            try:
                self.send_client(msg_id, status, code, msg, res_list)
            except bluetooth.btcommon.BluetoothError:
                self.parent.log.write(log.ERROR,
                                      "Failed to send to client -- "
                                      "disconnected? Restarting server...")
                self.disconnect()
                send_failed = True

            if status == evalcmd.STATUSEXIT or \
                    status == evalcmd.STATUSDISCONNECT:
                if not send_failed:
                    # already called if send_failed
                    self.parent.log.write(log.MESSAGE,
                                          "Got disconnect command.")
                    self.disconnect()

                    # end read_command() #

    def read_rows(self, count):
        """Read multiple rows from bluetooth socket.

        :param count: number of rows to read from BT
        :returns rows as list or empty list on BT error
        """

        # TODO this may loop forever -- do some max retries or so

        self.parent.led.set_led_yellow(1)

        result = []
        while 1:
            if len(result) == count:
                break

            # 1st try to read buffers for pending instructions
            while len(self.cmdbuffer):
                if len(result) == count:
                    break
                result.append(self.cmdbuffer.pop(0))

            if len(result) == count:
                break

            self.receive_into_buffer()

        self.parent.led.set_led_yellow(0)

        return result

        # end read_rows() #

    def receive_into_buffer(self):
        """

        """
        receiving = True
        while receiving:
            data = None
            # if last package was line head (num bytes), receive msg
            # if head size not set, receive 4 bytes (msg head)
            recv_size = self.next_buffer_size
            if recv_size == -1:
                recv_size = 4
                self.client_sock.settimeout(self.timeout)
            else:
                self.client_sock.settimeout(self.comm_timeout)
            if recv_size > 0:
                try:
                    data = self.client_sock.recv(recv_size)
                except bluetooth.btcommon.BluetoothError:
                    receiving = False
                    pass
            if data:
                if self.next_buffer_size == -1:
                    # we should have received buffer size now
                    try:
                        self.next_buffer_size = int(data)
                    except ValueError:
                        self.parent.log.write(log.EMERGENCY,
                                              "[RECV]: Value error in int "
                                              "conversion! Protocol broken?")
                else:
                    # we received data
                    self.cmdbuffer.append(data)
                    # self.parent.log.write(log.DEBUG3, "---<<< RECV: "+data)
                    self.next_buffer_size = -1

        self.client_sock.settimeout(self.timeout)

        # end receive_into_buffer() #

    def recv_ok_byte(self):
        """

        """
        self.client_sock.settimeout(self.comm_timeout)
        try:
            self.client_sock.recv(1)
        except bluetooth.btcommon.BluetoothError:
            return False
            pass
        return True
