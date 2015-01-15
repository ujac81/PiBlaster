"""alsamixer.py -- Set volume for master mixer and equalizer if found.



@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

import alsaaudio
import re
from subprocess import Popen, PIPE


class AlsaMixer:
    """Control alsa mixer master channel and equalizer plugin if found.
    """

    def __init__(self, main):
        """Get names of equalizer channels if such.
        """

        self.main = main
        self.mixers = alsaaudio.mixers()
        self.equal_channels = []  # names of equalizer channels if found

        self.init_equal_channels()

    @staticmethod
    def get_master_volume():
        """Get volume of alsa master channel for sound card #0
        :return: value between 0 and 100
        """
        # return alsaaudio.Mixer().getvolume()[0]
        return 50

    def set_master_volume(self, val):
        """Set volume of alsa master channel for sound card #0
        :param val: volume value in [0,100]
        """
        # alsaaudio.Mixer().setvolume(val)
        self.main.dbhandle.set_settings_value('vol_master',
                                              self.get_master_volume())

    def has_equalizer(self):
        """True if alsa device named 'equal' found.

        Requires installed plugequal alsa plugin.

        :return: True if equal mixer found.
        """
        return len(self.equal_channels) > 0

    def init_equal_channels(self):
        """Check if amixer -D equal returns list of equalizer channels.

        Will only work if alsa plugin equal loaded as 'equal'.
        """

        channels = Popen(["amixer", "-D", "equal", "scontrols"],
                         stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')

        self.equal_channels = []
        for chan in channels:
            m = re.search('\d+ k?Hz', chan)
            if m is not None:
                self.equal_channels.append(m.group(0))

    def get_equal_vals(self):
        """Get list of int values for equalizer channels.
        :return: [equal_channel_i_val([0..100]), ...]
        """
        if not len(self.equal_channels):
            return []

        channels = Popen(["amixer", "-D", "equal", "contents"],
                         stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')

        res = []
        for chan in channels:
            m = re.search('values=(\d+),(\d+)', chan)
            if m is not None:
                res.append((int(m.group(1)) + int(m.group(2))) / 2)
        return res

    def set_equal_channel(self, chan, val):
        """Set equalizer channel by channel id.

        Invokes `amixer -D equal cset numid=(chan+1) (val)`.

        :param chan: channel as integer value [0..N_channels-1].
        :param val: value between 0 and 100 -- int or string allowed.
        """
        if chan >= len(self.equal_channels):
            return

        Popen(["amixer", "-D", "equal", "cset", "numid=%d" % (chan+1),
               "%s" % val], stdout=PIPE, stderr=PIPE).communicate()

    def set_equal_channels(self, valstring):
        """Set all equalizer channels by space separated string.

        :param valstring: N_channels space separated values between 0 and 100.
        """
        vals = valstring.split()
        if len(vals) != len(self.equal_channels):
            return

        for i in range(len(vals)):
            self.set_equal_channel(i, vals[i])

        self.save_mixer()

    def restore_mixer(self):
        """Load mixer from config

        :return:
        """
        val = self.main.dbhandle.get_settings_value_as_int('vol_master', 50)
        self.set_master_volume(val)

        if not self.has_equalizer():
            return

        eqstr = self.main.dbhandle.get_settings_value('equalizer', '')
        if eqstr == '':
            return

        self.set_equal_channels(eqstr)

    def save_mixer(self):
        """save mixer settings to config

        :return:
        """
        self.main.dbhandle.set_settings_value('vol_master',
                                              self.get_master_volume())

        if not self.has_equalizer():
            return

        eqstr = ' '.join(self.get_equal_vals())
        self.main.dbhandle.set_settings_value('equalizer', eqstr)
