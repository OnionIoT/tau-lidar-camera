import array as arr

from ctypes import Structure, c_uint, c_ushort, c_uint8, c_uint16
import math

from .color import ColorMode, Color
from .frame import Frame

from .constants import *

NUM_COLORS    = 6000

LOW_AMPLITUDE = 16001
ADC_OVERFLOW  = 16002
SATURATION    = 16003
INTERFERENCE  = 16007
EDGE_DETECTED = 16008

k = 1
B0 = -0.125 * k - 0.25
B1 = B0 + 0.25 * k
B2 = B1 + 0.25 * k
B3 = B2 + 0.25 * k

G0 = B1
G1 = G0 + 0.25 * k
G2 = G1 + 0.25 * k
G3 = G2 + 0.25 * k + 0.125

R0 = B2
R1 = R0 + 0.25 * k
R2 = R1 + 0.25 * k
R3 = R2 + 0.25 * k + 0.25

def _interpolate(x, x0, y0, x1, y1) :
	if (x1 == x0) :
		return int(y0)
	else :
		return int(((float(x) - float(x0))*(float(y1) - float(y0)) / (float(x1) - float(x0)) + float(y0)))

class ImageColorizer :
    '''
    Helper class to color depth map.

    Methods
    -------
    setRange(index) :
        set distance range for coloring.
    getGrayscale(distance) :
        get grayscale based on distance value.
    getColor(distance) :
        get RGB color based on distance value.
    '''

    def __init__(self) :
        self.numSteps    = NUM_COLORS
        self.colorArray = []
        self._createColorMap()

    def setRange(self, start, stop) :
        '''
        set distance range for coloring.

        Parameters
        ----------
        start
            starting distance.
        stop
            stopping distance.
        '''
        self.begin = start
        self.end = stop
        self.indexFactorColor = float(NUM_COLORS) / (float(stop) - float(start))
        self.indexFactorBw = float(255) / (float(stop) - float(start))

    def _createColorMap(self) :

        red = green = blue = 0
        self.colorArray = []

        for indx in range(self.numSteps) :

            i = float(indx) / float(self.numSteps) - 0.25 * float(k)

            if (i >= R0 and i < R1) :
                red = _interpolate(i, R0, 0, R1, 255)
            elif (i >= R1 and i < R2) :
                red = 255
            elif (i >= R2) and i < R3 :
                red = _interpolate(i, R2, 255, R3, 0)
            else :
                red = 0

            if (i >= G0 and i < G1) :
                green = _interpolate(i, G0, 0, G1, 255)
            elif ((i >= G1) and (i<G2)) :
                green = 255
            elif ((i >= G2) and (i < G3)) :
                green = _interpolate(i, G2, 255, G3, 0)
            else :
                green = 0

            if (i >= B0 and i < B1) :
                blue = _interpolate(i, B0, 0, B1, 255)
            elif ((i >= B1) and (i < B2)) :
                blue = 255
            elif ((i >= B2) and (i < B3)) :
                blue = _interpolate(i, B2, 255, B3, 0)
            else :
                blue = 0

            color = Color(red, green, blue)

            self.colorArray.append(color)

    def getGrayscale(self, value) :
        '''
        get grayscale based on distance value.

        Parameters
        ----------
        value
            distance value in minimeters.
        '''
        color = float(value) * self.indexFactorBw
        return int(color)

    def getColor(self, value) :
        '''
        get RGB color based on distance value.

        Parameters
        ----------
        value
            distance value in minimeters.
        '''
        if (value == SATURATION) :
            return Color(255, 0, 128)
        elif (value == ADC_OVERFLOW) :
            return Color(169, 14, 255)
        elif (value == INTERFERENCE) :
            return Color(255, 255, 255)
        elif (value == EDGE_DETECTED) :
            return Color(0, 0, 0)
        elif (value == LOW_AMPLITUDE) :
            return Color(0, 0, 0)
        elif (value == 0) :
            return self.colorArray[0]

        value_float = float(value) - float(self.begin)
        if (value_float < 0 or value_float > self.end) :
            return Color(127, 127, 127)

        i = int(value_float * self.indexFactorColor) - 1
        i = self.numSteps - i - 1

        if (i < 0) :
            return self.colorArray[0]
        if (i >= NUM_COLORS) :
            return self.colorArray[NUM_COLORS - 1]

        c = self.colorArray[i]

        return c

class _PointMasked(Structure):
    _pack_ = 1
    _fields_ = [("grayscale", c_uint8), ("distance", c_uint16)]

ANGLE_X      = 50.0
ANGLE_Y      = 18.75

THETA_H = math.pi * ANGLE_X / 180.0
ALPHA_H = (math.pi - THETA_H) / 2

THETA_V = math.pi * ANGLE_Y / 180.0
ALPHA_V = 2 * math.pi - (THETA_V / 2)

class FrameBuilder:

    def __init__(self):
        self._imageColorizer = ImageColorizer()
        self._colorMode = ColorMode.DISTANCE
        self._imageColorizer.setRange(1000, 4000)

    def setColorMode(self, colorMode):
        self._colorMode = colorMode

    def setRange(self, z1, z2):
        self._imageColorizer.setRange(z1, z2)

    def composeFrame(self, dataArray) :
        '''
        compose Frame using raw bytearray data
        '''

        len_bytes = len(dataArray)
        if len_bytes < 28800:
            print("Bad frame ignored, bytes length: %d" % len_bytes)
            return None

        height = 60
        width  = 160

        data_depth_raw   = arr.array('f', [])
        data_grayscale   = arr.array('h', [])
        data_depth_rgb   = arr.array('h', [])
        saturated_mask   = arr.array('h', [])

        data_points = []

        _PointMasked9600 = 9600 * _PointMasked
        _points = _PointMasked9600.from_buffer(dataArray)

        i_data_point = 0
        for _p in _points:
            x = i_data_point % 160
            y = int(i_data_point / 160)

            distance = _p.distance  & MASK_OUT_CONFIDENCE
            grayscale = _p.grayscale & MASK_OUT_CONFIDENCE

            X = float("NaN")
            Y = float("NaN")
            Z = float("NaN")
            rgb = r = g = b = float("NaN")

            saturated_mask_v = 0
            c = self._imageColorizer.getColor(distance)

            if(
                distance < VALUE_LIMIT_VALID_PIXEL
                or
                distance == VALUE_ADC_OVERFLOW
                or
                distance == VALUE_SATURATION
            ):
                if (
                    distance == VALUE_ADC_OVERFLOW
                    or
                    distance == VALUE_SATURATION
                ):
                    saturated_mask_v = 255
                else:
                    if self._colorMode == ColorMode.GRAYSCALE:
                        r = g = b = grayscale
                    else:
                        r = c.r
                        g = c.g
                        b = c.b

                    rgb = r << 16 | g << 8 | b

                    gamma_i_h = ALPHA_H + x * (THETA_H / width)
                    gamma_i_v = ALPHA_V + y * (THETA_V / height)

                    Z = abs(0.001 * distance * math.sin(gamma_i_h))
                    Z = abs(Z * math.cos(gamma_i_v))

                    X = Z / math.tan(gamma_i_h)
                    Y = -1 * Z * math.tan(gamma_i_v)

                    data_points.append([X, Y, Z, r, g, b])

            saturated_mask.append(saturated_mask_v)

            data_depth_raw.append(Z)
            data_grayscale.append(grayscale)
            data_depth_rgb.extend([c.b, c.g, c.r])

            i_data_point += 1

        return Frame(height, width, data_depth_raw, data_depth_rgb, data_grayscale, data_points, dataArray)
