"""dirscanner.py -- scan directory for new items

"""

import mad
import os
import Queue
import sys
import threading
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError


class DirWorker(threading.Thread):
    """

    """

    def __init__(self, parent, queue, queue_lock, led_code):
        """

        """

        threading.Thread.__init__(self)

        self.parent = parent
        self.main = parent.main
        self.queue = queue
        self.queue_lock = queue_lock
        self.led_code = led_code
        self.db_entries = []
        self.cur_tot_bytes = 0

    def run(self):
        """

        """

        print("--- worker here! ---")

        while not self.queue.empty():
            self.queue_lock.acquire()
            item = None
            try:
                item = self.queue.get_nowait()
            except Queue.Empty:
                pass
            self.queue_lock.release()
            if item is not None:
                self.scan_dir(item[0], item[1])

        print("--- worker finished! ---")

    def scan_dir(self, dirid, path):
        """
        """
        mp3files = sorted([f for f in os.listdir(path)
                           if os.path.isfile(os.path.join(path, f))
                           and f.endswith(".mp3")])

        fileid = 1
        for f in mp3files:
            self.scan_mp3_file(dirid, fileid, path, f)
            fileid += 1

    def scan_mp3_file(self, dirid, fileid, path, filename):
        """
        """
        mp3path = os.path.join(path, filename)
        filename = os.path.basename(mp3path)
        extension = 'mp3'
        filename = filename[:-len(extension)-1]
        relpath = os.path.relpath(mp3path, self.parent.mnt_pnt)
        genre = u'Unknown Genre'
        year = 0
        title = filename
        album = u'Unknown Album'
        artist = u'Unknown Artist'
        length = 0

        sys.stdout.write('%d' % self.led_code)
        sys.stdout.flush()

        self.main.led.set_led(self.led_code, 1)

        try:
            tag = EasyID3(mp3path)
        except ID3NoHeaderError:
            tag = {}

        try:
            self.cur_tot_bytes += os.path.getsize(mp3path)
        except os.error:
            pass

        if 'album' in tag:
            album = tag['album'][0]
        if 'artist' in tag:
            artist = tag['artist'][0]
        if 'title' in tag:
            title = tag['title'][0]
        if 'genre' in tag:
            genre = tag['genre'][0]
        if 'date' in tag:
            try:
                year = int(tag['date'][0])
            except ValueError:
                year = 0
        if 'length' in tag:
            try:
                length = int(tag['length'][0]) / 1000
            except ValueError:
                length = 0
        else:
            mf = mad.MadFile(mp3path)
            length = mf.total_time() / 1000

        disptitle = u'%s - %s' % (artist, title)
        if artist == u'Unknown Artist':
            disptitle = title

        self.db_entries.append([fileid, dirid, self.parent.storid, relpath,
                                filename, extension, genre, year, title,
                                album, artist, length, disptitle])

        self.main.led.set_led(self.led_code, 0)


class DirScanner:
    """

    """

    def __init__(self, parent, mnt_pnt, storid):
        """

        """

        self.parent = parent
        self.main = parent.main
        self.mnt_pnt = mnt_pnt
        self.storid = storid
        self.queue = Queue.Queue()
        self.queue_lock = threading.Lock()
        self.cur_dir_id = 0

        self.workers = []

        # create worker threads, but don't start until queue is filled
        for led_code in range(4):
            self.workers.append(
                DirWorker(self, self.queue, self.queue_lock, led_code))

    def scan(self):
        """
        """
        # fill queue -- flash yellow led while dir scan
        self.main.led.set_led_yellow(1)
        self.queue_lock.acquire()
        print("--fill--")
        self.recursive_fill_queue(self.mnt_pnt, 'root', -1)
        print("--fill done--")
        self.queue_lock.release()
        self.main.led.set_led_yellow(0)

        print("--workers start--")

        # start workers
        self.start()

        # wait for workers -- this will block main app!
        # TODO: do some smarter stuff here
        self.join()

        print("--workers joined--")

        self.main.led.set_led_yellow(1)
        self.main.dbhandle.con.commit()
        self.main.led.set_led_yellow(0)

    def recursive_fill_queue(self, path, dirname, parentid):
        """
        """
        print("--fill %s--" % path)
        dirs = sorted([f for f in os.listdir(path)
                       if os.path.isdir(os.path.join(path, f))])

        dirpath = os.path.relpath(path, self.mnt_pnt)
        dirid = self.cur_dir_id
        self.cur_dir_id += 1

        self.queue.put([dirid, path])

        if parentid >= 0:
            # TODO: dirname twice -- path should be there for id reassignment.
            self.main.dbhandle.cur.execute(
                'INSERT INTO Dirs VALUES (?, ?, ?, ?, ?, ?, ?)',
                (dirid, parentid, self.storid, 0, 0, dirname, dirpath))

        for d in dirs:
            subdir = os.path.join(path, d)
            self.recursive_fill_queue(subdir, d, dirid)

    def start(self):
        """

        """
        for t in self.workers:
            t.start()

    def join(self):
        """

        """
        for t in self.workers:
            t.join()
            print("Insert -- %d " % len(t.db_entries))
            self.main.led.set_led(t.led_code, 1)
            if len(t.db_entries):
                self.main.dbhandle.cur.\
                    executemany('INSERT INTO Fileentries VALUES (?, ?, ?, ?, '
                                '?, ?, ?, ?, ?, ?, ?, ?, ?)', t.db_entries)
            self.main.led.set_led(t.led_code, 0)











