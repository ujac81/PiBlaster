"""playlist.py -- Manage list of PlayListItem

@Author Ulrich Jansen <ulrich.jansen@rwth-aachen.de>
"""


import log



class PlayList:


  def __init__(self, parent, row):
    """
    """

    self.parent = parent

    self.playlist = []
    self.position = 0

    self.index    = row[0]
    self.name     = row[1]
    self.created  = row[2]
    self.creator  = row[3]
    self.itemcnt  = row[4]
    self.position = row[5]

    self.load_items()




  def load_items(self):
    """
    """



