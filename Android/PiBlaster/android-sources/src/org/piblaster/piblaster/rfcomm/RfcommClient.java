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
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;

import java.util.Set;

public class RfcommClient extends org.qtproject.qt5.android.bindings.QtActivity
{
    private static NotificationManager m_notificationManager;
    private static Notification.Builder m_builder;
    private static RfcommClient m_instance;
    private BluetoothAdapter m_BluetoothAdapter;

    // Intent request codes
    private static final int REQUEST_CONNECT_DEVICE = 1;
    private static final int REQUEST_ENABLE_BT = 2;

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        switch (requestCode) {
            case REQUEST_ENABLE_BT:
                if (resultCode == Activity.RESULT_OK) {
                    // Do nothing, QML App should reask for hasBluetooth()
                    // and we should be fine.
                } else {
                    // User did not enable Bluetooth or an error occurred.
                }
            break;

            default:
                super.onActivityResult(requestCode, resultCode, data);
                break;
        }
    }


    public RfcommClient()
    {
        System.out.println("RfcommClient ctor");
        m_instance = this;
        m_BluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    }

    public void requestBluetooth()
    {
        System.out.println("RfcommClient requestBluetooth()");
        if (m_BluetoothAdapter == null) {
            return;
        }
        if (m_BluetoothAdapter.isEnabled()) {
            return;
        }
        else {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
        }
    }

    public void testBluetooth() {
        System.out.println("RfcommClient testBluetooth(): " + hasBluetooth());
    }


    public int hasBluetooth() {

        System.out.println("RfcommClient hasBluetooth()");
        if (m_BluetoothAdapter == null) {
            m_BluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
            if (m_BluetoothAdapter == null) {
                return -1;
            }
        }
        System.out.println("Adapter enabled: " + m_BluetoothAdapter.isEnabled());
        if (m_BluetoothAdapter.isEnabled()) {

            Set<BluetoothDevice> pairedDevices = m_BluetoothAdapter.getBondedDevices();
            // If there are paired devices
            if (pairedDevices.size() > 0) {
                // Loop through paired devices
                for (BluetoothDevice device : pairedDevices) {
                    // Add the name and address to an array adapter to show in a ListView
                    System.out.println("Found: " + device.getName() + " -- " + device.getAddress());
                    //mArrayAdapter.add(device.getName() + "\n" + device.getAddress());
                }
            }
            else {
                System.out.println("No paired");
            }
            return -3;
        }
        else {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            return -2;
        }
    }

    public void notify(String s)
    {

        System.out.println("RfcommClient notify: " + s);


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
