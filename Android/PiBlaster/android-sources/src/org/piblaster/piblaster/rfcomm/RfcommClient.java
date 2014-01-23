/****************************************************************************
**
** Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
** Contact: http://www.qt-project.org/legal
**
** This file is part of the QtAndroidExtras module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and Digia.  For licensing terms and
** conditions see http://qt.digia.com/licensing.  For further information
** use the contact form at http://qt.digia.com/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** In addition, as a special exception, Digia gives you certain additional
** rights.  These rights are described in the Digia Qt LGPL Exception
** version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3.0 as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU General Public License version 3.0 requirements will be
** met: http://www.gnu.org/copyleft/gpl.html.
**
**
** $QT_END_LICENSE$
**
****************************************************************************/

package org.piblaster.piblaster.rfcomm;

import android.app.Activity;
import android.app.Notification;
import android.app.NotificationManager;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.Method;
import java.lang.StringBuilder;
import java.util.UUID;
import java.util.Set;
import java.util.Vector;


public class RfcommClient extends org.qtproject.qt5.android.bindings.QtActivity
{
    private static final String TAG = "RfcommClient.java";

    private static final int BT_NOT_INITIALIZED     = -100;
    private static final int BT_NOT_ENABLED         = -1;
    private static final int BT_NO_SOCKET           = -2;
    private static final int BT_NO_CONNECT          = -3;
    private static final int BT_NO_CLEANCONNECT     = -4;
    private static final int BT_NO_STREAMS          = -5;
    private static final int BT_NO_AUTH             = -10;
    private static final int BT_ERR_STREAM_WRITE    = -11;
    private static final int BT_ERR_STREAM_READ     = -12;
    private static final int BT_ERR_STREAM_INCOMPL  = -13;
    private static final int BT_DISCONNECTED        = -20;

    private static final int BT_DEV_ENABLED         = 1;
    private static final int BT_CONNECTED           = 2;
    private static final int BT_AUTH_OK             = 3; // state should be 3 for functional connection


    private static NotificationManager m_notificationManager;
    private static Notification.Builder m_builder;
    private static BluetoothAdapter m_BluetoothAdapter = null;
    private static BluetoothSocket m_btSocket = null;
    private static OutputStream m_outStream = null;
    private static InputStream m_inStream = null;
    private static RfcommClient m_instance;

    // Intent request codes
    private static final int REQUEST_CONNECT_DEVICE = 1;
    private static final int REQUEST_ENABLE_BT = 2;




    private static int m_bluetoothstatus = BT_NOT_INITIALIZED;

    private static Vector<String> m_bluetoothmessages = new Vector<String>();
    private static Vector<String> m_rfcommMsg = new Vector<String>();
    private static String m_rfcommStatusMsg = "";
    private static int m_rfcommStatus = -1;


    // MAC for Pi bluetooth device, set via APP settings
    private static String m_pibt_address = "00:1A:7D:DA:71:14";
    // UUID for pyblaster service
    private static final UUID MY_UUID = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");
    // password for pyblaster servie
    private static String m_pibt_passwd = "1234";


    public RfcommClient() {
        m_instance = this;
    }


    public static int bluetoothMessagesCount() { return m_bluetoothmessages.size(); }
    public static String bluetoothMessage(int i) { return m_bluetoothmessages.get(i); }

    public static int rfcommMessagesCount() { return m_rfcommMsg.size(); }
    public static String rfcommMessage(int i) { return m_rfcommMsg.get(i); }


    public static int bluetoothConnectionStatus() { return m_bluetoothstatus; }



    /**
     * @brief Called when the activity is first created.
     *
     *
     */
    public static void onInit() {
        m_BluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        checkBTState();
    }

    /**
     * @brief Callback for activate bluetooth request
     *
     *
     */
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        switch (requestCode) {
            case REQUEST_ENABLE_BT:
                if (resultCode == Activity.RESULT_OK) {
                    m_bluetoothstatus = BT_DEV_ENABLED;
                    m_bluetoothmessages.add("...Bluetooth now on...");
                    Log.d(TAG, "BT Callback: ...Bluetooth now on...");
                } else {
                    // User did not enable Bluetooth or an error occurred.
                    m_bluetoothstatus = BT_NOT_ENABLED;
                    m_bluetoothmessages.add("BT Callback: ...Bluetooth failed...");
                    Log.d(TAG, "...Bluetooth failed...");
                }
            break;

            default:
                super.onActivityResult(requestCode, resultCode, data);
                break;
        }
    }


    /**
     * @brief Check for Bluetooth support and then check to make sure it is turned on
     * Emulator doesn't support Bluetooth and will return null
     */
    private static void checkBTState() {

        if(m_BluetoothAdapter==null) {
            Log.d(TAG, "Bluetooth not supported");
        } else {
            if (m_BluetoothAdapter.isEnabled()) {
                m_bluetoothstatus = 1;
                m_bluetoothmessages.add("CHECK ...Bluetooth ON...");
                Log.d(TAG, "...Bluetooth ON...");
            } else {
                //Prompt user to turn on Bluetooth
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                m_instance.startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }
        }
    }

    public static int disableBT() {
        if(m_BluetoothAdapter != null) {
            m_BluetoothAdapter.disable();
            return 0;
        }
        return 1;
    }


    /**
     * @brief Connect to PyBlaster service
     * Called via RFCOMMClient::tryConnect()
     *
     */
    public static int tryConnect() {

        Log.d(TAG, "try connect..." + m_bluetoothstatus);

        // retry turning on adapter
        if (m_bluetoothstatus == BT_NOT_INITIALIZED || m_bluetoothstatus == BT_NOT_ENABLED)
        {
            checkBTState();
            m_bluetoothmessages.add("BT TRY CONNECT no status.");
            m_bluetoothstatus = BT_NOT_ENABLED; // adapter not available
            return m_bluetoothstatus;
        }

        BluetoothDevice device = m_BluetoothAdapter.getRemoteDevice(m_pibt_address);

        Log.d(TAG, device.toString());

        try {
            m_btSocket = device.createInsecureRfcommSocketToServiceRecord(MY_UUID);
        } catch (IOException e1) {
            Log.d(TAG, "ERROR socket create failed: " + e1.getMessage());
            m_bluetoothmessages.add("BT TRY CONNECT create rfcomm socket failed: " + e1.getMessage());
            m_bluetoothstatus = BT_NO_SOCKET; // rfcomm service not available
            return m_bluetoothstatus;
        }

        m_BluetoothAdapter.cancelDiscovery();

        // Establish the connection.  This will block until it connects.
        Log.d(TAG, "...Connecting...");
        try {
            m_btSocket.connect();
            Log.d(TAG, "...Connection ok...");
            m_bluetoothmessages.add("BT TRY CONNECT ok.");
        } catch (IOException e) {
            try {
                m_btSocket.close();
            } catch (IOException e2) {
                Log.d(TAG, "Fatal Error: unable to close socket during connection failure: " + e2.getMessage() + ".");
                m_bluetoothstatus = BT_NO_CLEANCONNECT; // closing failed while connecting
                m_bluetoothmessages.add("BT TRY CONNECT ERROR while closing socket: "+ e2.getMessage() + ".");
                return m_bluetoothstatus;
            }
            Log.d(TAG, "Fatal Error: unable to connect: " + e.getMessage() + ".");
            m_bluetoothmessages.add("BT TRY CONNECT ERROR unable to connect: "+ e.getMessage() + ".");
            m_bluetoothstatus = BT_NO_CONNECT; // could not create socket
            return m_bluetoothstatus;
        }

        // Create a data stream so we can talk to server.
        Log.d(TAG, "...Create Socket...");
        try {
            m_outStream = m_btSocket.getOutputStream();
            m_inStream = m_btSocket.getInputStream();
        } catch (IOException e) {
            Log.d(TAG, "Fatal Error: stream creation failed:" + e.getMessage() + ".");
            m_bluetoothmessages.add("BT TRY CONNECT ERROR unable to get streams: "+ e.getMessage() + ".");
            m_bluetoothstatus = BT_NO_STREAMS; // could not establish byte stream
            return m_bluetoothstatus;
        }

        Log.d(TAG, "connected...");
        m_bluetoothmessages.add("BT TRY CONNECT connected.");

        m_bluetoothstatus = BT_CONNECTED; // connected, but not authenticated

        sendReceive(m_pibt_passwd);

        // Try to authenticate
        if (m_rfcommStatus == 0) {
            m_bluetoothstatus = BT_AUTH_OK; // authenticated
            Log.d(TAG, "BT AUTH GOOD.");
            m_bluetoothmessages.add("BT AUTH OK");
        } else {
            m_bluetoothstatus = BT_NO_AUTH; // wrong pw
            Log.d(TAG, "BT AUTH BAD.");
            m_bluetoothmessages.add("BT AUTH WRONG PASSWORD");
            try {
                m_btSocket.close();
            } catch (IOException e) {
                Log.d(TAG, "Fatal Error: while closing socket:" + e.getMessage() + ".");
                m_bluetoothmessages.add("BT ERROR while closing socket: "+ e.getMessage() + ".");
                m_bluetoothstatus = BT_NO_CLEANCONNECT;
            }
        }

        return m_bluetoothstatus;
    }

    /**
     * @brief Prepare multiple row command like "plappendmultiple MODE N_ROWS"
     * @return 0 if send ok
     */
    public static int prepareMassSend(String initCmd) {

        if (m_bluetoothstatus < 2) {
            // not connected
            m_bluetoothmessages.add("BT ERROR tried to send on closed connection");
            return -1;
        }
        try {
            m_outStream.write(initCmd.getBytes());
        } catch (IOException e) {
            Log.d(TAG, "Fatal Error: outstream.write: " + e.getMessage() + ".");
            m_bluetoothmessages.add("BT ERROR cannot write to stream: "+ e.getMessage() + ".");
            m_bluetoothstatus = BT_ERR_STREAM_WRITE;
            return m_bluetoothstatus;
        }
        return 0;
    }


    /**
     * @brief Send single row while in mass send mode -- need to call prepareMassSend() before
     */
    public static int sendSingleRow(String row) {
        if (m_bluetoothstatus < 2) {
            // not connected
            m_bluetoothmessages.add("BT ERROR tried to send on closed connection");
            return -1;
        }
        row += " !EOL! ";
        try {
            m_outStream.write(row.getBytes());
        } catch (IOException e) {
            Log.d(TAG, "Fatal Error: outstream.write: " + e.getMessage() + ".");
            m_bluetoothmessages.add("BT ERROR cannot write to stream: "+ e.getMessage() + ".");
            m_bluetoothstatus = BT_ERR_STREAM_WRITE;
            return m_bluetoothstatus;
        }
        return 0;
    }

    /**
     * @brief Wait for answer from PyBlaster after sending multiple commands via prepareMassSend() and sendSingleRow()
     *
     * Result may be parsed by rfcommMessage(0|1)
     * @return should be 2 if everything ok
     */
    public static int waitForMassCommand() {
        long startTime = System.currentTimeMillis();
        m_rfcommMsg.clear();

        if (m_bluetoothstatus < 2) {
            // not connected
            m_bluetoothmessages.add("BT ERROR tried to send on closed connection");
            return -1;
        }

        // read return value and return msg

        boolean doRead = true;
        int status = -1;

        // @todo prevent loop from deadlocking + add timeouts to readLine()
        while ( doRead ) {
            String[] input = readLine().split(" !EOL! ");

            if (m_bluetoothstatus < 2) {
                Log.d(TAG, "STREAM DIED");
                m_bluetoothmessages.add("BT ERROR stream died.");
                break;
            }

            for (int i = 0; i < input.length; i++) {
                m_rfcommMsg.add(input[i].trim());
            }
            if (m_rfcommMsg.size() >= 3) {
                try {
                    m_rfcommStatus = Integer.parseInt(m_rfcommMsg.get(0));
                    m_rfcommStatusMsg = m_rfcommMsg.get(1);
                } catch (NumberFormatException e) {
                    Log.d(TAG, "Fatal Error: wrong number format");
                    m_bluetoothmessages.add("BT ERROR faulty numbers from stream");
                }
                doRead = false;
            }
        }

        long durTime = System.currentTimeMillis() - startTime;
        m_bluetoothmessages.add("BT multi command executed in '" + durTime + "ms");

        return m_rfcommMsg.size();
    }






    public static int sendReceive(String msg) {

        long startTime = System.currentTimeMillis();
        m_rfcommMsg.clear();

        if (m_bluetoothstatus < 2) {
            // not connected
            m_bluetoothmessages.add("BT ERROR tried to send on closed connection");
            return -1;
        }

        try {
            m_outStream.write(msg.getBytes());
        } catch (IOException e) {
            Log.d(TAG, "Fatal Error: outstream.write: " + e.getMessage() + ".");
            m_bluetoothmessages.add("BT ERROR cannot write to stream: "+ e.getMessage() + ".");
            m_bluetoothstatus = BT_ERR_STREAM_WRITE;
            return m_bluetoothstatus;
        }

        // read return value, return msg, return list size and return list

        boolean doRead = true;
        int linecnt = -1;
        int status = -1;
        m_rfcommMsg.clear();

        // @todo prevent loop from deadlocking + add timeouts to readLine()
        while ( doRead ) {
            String[] input = readLine().split(" !EOL! ");

            if (m_bluetoothstatus < 2) {
                Log.d(TAG, "STREAM DIED");
                m_bluetoothmessages.add("BT ERROR stream died.");
                break;
            }

            for (int i = 0; i < input.length; i++) {
                m_rfcommMsg.add(input[i].trim());
            }
            if (m_rfcommMsg.size() >= 3 && linecnt == -1) {
                try {
                    linecnt = Integer.parseInt(m_rfcommMsg.get(2));
                    m_rfcommStatus = Integer.parseInt(m_rfcommMsg.get(0));
                    m_rfcommStatusMsg = m_rfcommMsg.get(1);
                } catch (NumberFormatException e) {
                    Log.d(TAG, "Fatal Error: wrong number format");
                    m_bluetoothmessages.add("BT ERROR faulty numbers from stream");
                }
            }

            if (linecnt != -1 && m_rfcommMsg.size() == linecnt + 3) {
                doRead = false;
            }
        }

        long durTime = System.currentTimeMillis() - startTime;

        String short_cmd = msg;
        if ( short_cmd.length() > 20 )
            short_cmd = msg.substring(0, 19) + "...";

        m_bluetoothmessages.add("BT command '" + short_cmd + "' executed in '" + durTime + "ms");


        return m_rfcommMsg.size();
    }

    public static int disconnect() {

        if (m_bluetoothstatus < 3) { return -2; } // not connected

        sendReceive("disconnect");
        m_bluetoothstatus = BT_DISCONNECTED;
        m_bluetoothmessages.add("BT DISCONNECTED.");

        try {
            m_btSocket.close();
        } catch (IOException e) {
            Log.d(TAG, "Fatal Error: while closing socket:" + e.getMessage() + ".");
            m_bluetoothmessages.add("BT ERROR while closing socket: "+ e.getMessage() + ".");
            m_bluetoothstatus = BT_NO_CLEANCONNECT;
        }
        if ( m_rfcommStatus == 101 ) { return 0; } // disconnect ok
        return -1; // disconnect failed somehow
    }

    private static String readLine() {
        String line = "";

        if (m_bluetoothstatus < 2) { return line; } // not connected

        Reader in;
        try {
             in = new InputStreamReader(m_inStream, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            Log.d(TAG, "Fatal Error: SHOULD NEVER HAPPEN: NO UTF-8");
            m_bluetoothstatus = BT_NO_STREAMS;
            return line;
        }

        char[] buffer = new char[1024];
        StringBuilder out = new StringBuilder();
        try {
            int bytes = in.read(buffer, 0, 1024);
            if (bytes > 0) {
                out.append(buffer, 0, bytes);
                line = out.toString();
                Log.d(TAG, "==== READ LINE: --" + line + "--");
            }
        } catch (IOException e) {
            Log.d(TAG, "Fatal Error: read stream" + e.getMessage() + ".");
            m_bluetoothmessages.add("BT ERROR cannot read from stream: "+ e.getMessage() + ".");
            m_bluetoothstatus = BT_NO_STREAMS;
        }
        return line;
    }


    public static void notify(String s)
    {
        if (m_notificationManager == null) {
            m_notificationManager = (NotificationManager)m_instance.getSystemService(Context.NOTIFICATION_SERVICE);
            m_builder = new Notification.Builder(m_instance);
            m_builder.setSmallIcon(R.drawable.icon);
            m_builder.setContentTitle("A message from Qt!");
        }
        m_builder.setContentText(s);
        m_notificationManager.notify(1, m_builder.build());
    }
}
