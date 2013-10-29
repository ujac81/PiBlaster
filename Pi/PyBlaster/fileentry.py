"""fileentry.py -- Object to represent a single mp3 file

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from mutagen.easyid3 import EasyID3
import os


class FileEntry:
  """Object to represent a single mp3 file

  Handled inside Direntry for the corresponding directory.
  """

  def __init__(self, path, file_id, dbrebuild=False):
    """Initialize attributes, if not in rebuild mode, scan ID3 tag data."""

    self.path         = path
    self.valid        = 1
    self.file_id      = file_id   # [storage_id, dir_id, file_id]
    self.length       = 0

    if dbrebuild:
      return

    self.filename     = os.path.basename(path)
    self.extension    = os.path.splitext(self.filename)[1].replace('.', '')
    self.filename     = self.filename[:-len(self.extension)-1]
    self.playtimes    = 0
    self.GENRE        = u'Unknown Genre'
    self.YEAR         = 0
    self.TITLE        = self.filename
    self.ALBUM        = u'Unknown Album'
    self.ARTIST       = u'Unknown Artist'

    tag = EasyID3(path)

    if 'album'  in tag: self.ALBUM  = tag['album'][0]
    if 'artist' in tag: self.ARTIST = tag['artist'][0]
    if 'title'  in tag: self.TITLE  = tag['title'][0]
    if 'genre'  in tag: self.GENRE  = tag['genre'][0]
    if 'date'   in tag:
      try:
        self.YEAR = int(tag['date'][0])
      except exceptions.ValueError:
        self.YEAR = 0
    if 'length' in tag:
      try:
        self.length = int(tag['length'][0]) / 1000
      except exceptions.ValueError:
        self.length = 0

    # end __init__() #

  def print_file(self):
    """Do not use __str__ as it will fuck up on strange unicode chars
    """
    print("[%d,%d,%d] %s - %s - %s (%s, %d) %d" %
          (self.file_id[0], self.file_id[1], self.file_id[2], self.ARTIST,
           self.ALBUM, self.TITLE, self.GENRE, self.YEAR, self.length))

    # end print_file() #
