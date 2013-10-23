"""fileentry.py


@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""

from ID3 import *
#import mad
from mutagen.mp3 import MP3
import os


class FileEntry:
  """
  """

  def __init__(self, path, file_id, dbrebuild=False):
    """
    """
    self.path         = path
    self.valid        = 1
    self.file_id      = file_id   # [storage_id, dir_id, file_id]
    self.length       = 0

    if dbrebuild: return

    self.filename     = os.path.basename(path)
    self.extension    = os.path.splitext(self.filename)[1].replace('.', '')
    self.filename     = self.filename[:-len(self.extension)-1]
    self.playtimes    = 0
    self.GENRE        = u'Unknown Genre'
    self.YEAR         = 0
    self.TITLE        = self.filename
    self.ALBUM        = u'Unknown Album'
    self.ARTIST       = u'Unknown Artist'

    try:
      id3info = ID3(path)
      for k, v in id3info.items():
        if k == 'TITLE'  : self.TITLE  = v
        if k == 'ALBUM'  : self.ALBUM  = v
        if k == 'ARTIST' : self.ARTIST = v
        if k == 'GENRE'  : self.GENRE  = v
        if k == 'YEAR'   :
          try:
            self.YEAR = int(v)
          except exceptions.ValueError:
            self.YEAR = 0
    except InvalidTagError, message:
      self.valid = 0

    #mf = mad.MadFile(path)
    #self.length = mf.total_time()
    audio = MP3(path)
    self.length = int(audio.info.length*1000)


    self.fix_all_encodings()

    # end __init__() #

  def fix_encoding(self, inputstr):
    """
    """
    #return unicode(inputstr.encode(u'utf-8'), u'iso-8859-1')
    try:
      inputstr = unicode(inputstr)
    except UnicodeDecodeError:
      inputstr = inputstr.decode('latin-1')

    return inputstr

  def fix_all_encodings(self):
    """
    """
    self.filename = self.fix_encoding(self.filename)
    self.GENRE    = self.fix_encoding(self.GENRE)
    self.TITLE    = self.fix_encoding(self.TITLE)
    self.ALBUM    = self.fix_encoding(self.ALBUM)
    self.ARTIST   = self.fix_encoding(self.ARTIST)


  def print_file(self):
    """Do not use __str__ as it will fuck up on strange unicode chars
    """
    print("[%d,%d,%d] %s - %s - %s (%s, %d) %d" % (self.file_id[0], self.file_id[1], self.file_id[2], self.ARTIST, self.ALBUM, self.TITLE, self.GENRE, self.YEAR, self.length))
