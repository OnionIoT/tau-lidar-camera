import binascii

from .constants import *
from .util import *
from .communication import Communication
from TauLidarCommon.d3 import FrameBuilder
from TauLidarCommon.color import ColorMode, Color
from .info import CameraInfo
from TauLidarCommon.frame import FrameType, Frame

class Camera :
    '''
    ToF camera, access point to the ToF sensor.

    Attributes
    ----------
    _cameraInfo :
        CameraInfo.

    Methods
    -------
    open(port=None)
        open communication to the ToF sensor.
    close()
        close communication to the ToF sensor.
    setDefaultParameters()
        convenient method to set default parameters.
    getChipInformation()
        request Chip Information.
    getFirmwareRelease()
        request Firmware Release.
    info():
        get camera info
    readFrame(acquisitionMode, opMode, hdr)
        request new image.
    '''

    _frameBuilder = FrameBuilder()

    def __init__(self):
        self._comm = Communication()

    @staticmethod
    def open(port=None):
        '''
        open communication to the sensor via serial port.

        Parameters
        ----------
        port : str, optional
            serial port the sensor connected. if there is no port given, the first available sensor will be used.

        Returns
        ----------
        Camera
            An instance of Camera object which connected to the ToF sensor

        Raises
        ----------
        Exception
            Error to open the camera.
        '''

        camera = Camera()
        return camera._open(port)

    def _open(self, port=None):

        if self._comm._ser.is_open :
            raise Exception("Camera is already opened!")

        self._comm.open(port)

        if self._comm._ser.is_open: 
            self.setDefaultParameters()

        return self

    def info(self):
        '''
        get camera information.
        '''

        chipType, chipVersion = self.getIdentification()
        model = "%d.%d" % (chipType, chipVersion)

        major, minor = self.getFirmwareRelease()
        firmware = "%d.%d" % (major, minor)

        waferId, chipId = self.getChipInformation()
        uid = "%d.%d" % (waferId, chipId)

        return CameraInfo(model, firmware, uid, "160x60",  self._comm._ser.port)

    def close(self) :
        '''
        close communication to the sensor.
        '''

        self._comm.close()

    def setDefaultParameters(self) :
        '''
        set default parameters.
        '''
        self.setModulationFrequency(VALUE_20MHZ) ## frequency: 20MHZ
        self.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
        self.setMode(0)                          ## Mode 0, wide fov
        self.setHdr(0)                           ## HDR off
        self.setIntegrationTime3d(0, 800)        ## set integration time 0: 1000
        self.setIntegrationTimeGrayscale(5000)   ## set integration time grayscale: 20000
        self.setMinimalAmplitude(0, 60)          ## set minimal amplitude 0: 80
        self.setOffset(0)                        ## set distance offset: 0
        self.setRoi(0, 0, 159, 59)               ## set ROI to max width and height
        
        ## static
        Camera.setColorMode(ColorMode.DISTANCE)
        Camera.setRange(0, 7500)

    def setModulationFrequency(self, frequency):
        self._comm.setModulationFrequency(frequency)

    def setModulationChannel(self, channel):
        self._comm.setModulationChannel(0, channel)

    def setMode(self, mode):
        self._comm.setMode(mode)

    def setHdr(self, hdr):
        self._comm.setHdr(hdr)

    def setIntegrationTime3d(self, index, t):
        self._comm.setIntegrationTime3d(index, t)

    def setIntegrationTimeGrayscale(self, t):
        self._comm.setIntegrationTimeGrayscale(t)

    def setMinimalAmplitude(self, index, t):
        self._comm.setMinimalAmplitude(index, t)

    def setOffset(self, offset):
        self._comm.setOffset(offset)

    def setRoi(self, x0, y0, x1, y1):
        self._comm.setRoi(x0, y0, x1, y1)

    @staticmethod
    def setColorMode(colorMode):
        Camera._frameBuilder.setColorMode(colorMode)

    @staticmethod
    def setRange(z1, z2):
        Camera._frameBuilder.setRange(z1, z2)

    def getChipInformation(self) :
        '''
        request Chip Information.
        '''
        dataArray = self._comm.getChipInformation()
        waferId = getUint16LittleEndian(dataArray, INDEX_WAFER_ID - COMMAND_SIZE_HEADER)
        chipId  = getUint16LittleEndian(dataArray, INDEX_CHIP_ID  - COMMAND_SIZE_HEADER)

        return (waferId, chipId)

    def getIdentification(self) :
        '''
        request Chip Information.
        '''
        dataArray = self._comm.getIdentification()
        identificationValue = int(binascii.hexlify(dataArray), 16)
        chipType = (identificationValue & MASK_CHIP_TYPE_DEVICE) >> SHIFT_CHIP_TYPE_DEVICE
        chipVersion = (identificationValue & MASK_VERSION) >> SHIFT_VERSION

        return (chipType, chipVersion)

    def getFirmwareRelease(self) :
        '''
        request Firmware Release.
        '''
        dataArray = self._comm.getFirmwareRelease()
        firmware = getUint32LittleEndian(dataArray, 0)
        major = getValueMsb(firmware)
        minor = getValueLsb(firmware)
        return (major, minor)

    def readFrameRawData(self, frameType) :
        '''
        request a new raw data of a frame from sensor.
        to compose Frame from raw data using FrameBuilder.composeFrame in d3.py.
        '''
        
        if frameType == FrameType.DISTANCE_GRAYSCALE:
            dataArray = self._comm.getDistanceGrayscale()
            return dataArray[TOF_635_IMAGE_HEADER_SIZE : len(dataArray)]

        elif frameType == FrameType.DISTANCE_AMPLITUDE:
            dataArray = self._comm.getDistanceAmplitude()
            return dataArray[TOF_635_IMAGE_HEADER_SIZE : len(dataArray)]

        elif frameType == FrameType.DISTANCE:
            dataArray = self._comm.getDistance()
            return dataArray[TOF_635_IMAGE_HEADER_SIZE : len(dataArray)]

    @staticmethod
    def composeFrame(dataArray, frameType) :
        '''
        compose Frame using raw bytearray data
        '''
        
        return Camera._frameBuilder.composeFrame(dataArray, frameType)

    def readFrame(self, frameType=FrameType.DISTANCE_GRAYSCALE) :
        '''
        A convenient method to directly get a new frame, it is an expensive call, 
        alternatively use readFrameRawData and compose Frame from a separate thread.
        '''
        
        dataArray = self.readFrameRawData(frameType)

        return Camera.composeFrame(dataArray, frameType)
