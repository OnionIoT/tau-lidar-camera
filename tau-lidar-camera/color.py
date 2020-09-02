
from enum import Enum

class ColorMode(Enum):
    '''
    ColorMode mode Enum
    '''
    DISTANCE  = 0  ## psedo distance color
    GRAYSCALE = 1  ## grayscale

class Color :
    '''
    RGB color.
    
    Attributes
    ----------
    r : 
        red.
    g : 
        green.
    b : 
        blue.
    '''
    def __init__(self) : 
        self.r = 0
        self.g = 0
        self.b = 0
    def __init__(self, r_, g_, b_) : 
        self.r = r_
        self.g = g_
        self.b = b_

