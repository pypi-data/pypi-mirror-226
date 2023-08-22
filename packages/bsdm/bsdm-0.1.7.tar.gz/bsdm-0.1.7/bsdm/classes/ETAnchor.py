from svgwrite import cm, mm, px  

import utils.config as config

from utils.logger import LOGGER

from classes.Drawing import Drawing



from enum import Enum, auto

class ETAnchorPosition(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class ETAnchor(object):
    
    def __init__(self):
        pass