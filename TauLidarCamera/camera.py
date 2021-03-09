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
    ToF camera class, access point to the ToF camera.

    TauLidarCamera library depends on the TauLidarCommon library.

    If you install TauLidarCamera using pip (pip install TauLidarCamera), TauLidarCommon library will be automaticall installed. 
    
    To initiate an instance of Camera object, call static method of Camera.open(port=None).
    '''

    _frameBuilder = FrameBuilder()

    def __init__(self):
        self._comm = Communication()

    @staticmethod
    def open(port=None):
        '''
        open communication to the camera via serial port.

        By default, Camera will connect to the first available ToF device. 
        Alternatively can specify serial port '/dev/ttyACM0': 
        
            Camera.open('/dev/ttyACM0')

        Parameters
        ----------
        port : str, optional
            serial port the camera connected. if there is no port given, the first available camera will be used.

        Returns
        ----------
        Camera
            An instance of Camera object which connected to the ToF camera.

        Raises
        ----------
        Exception
            Error to open the camera.
        '''

        camera = Camera()
        return camera._open(port)

    @staticmethod
    def scan():
        '''
        scan for available Tau LiDAR cameras


        Parameters
        ----------
        None

        Returns
        ----------
        ports
            A list of serial port device name that represents Tau cameras

        '''

        camera = Camera()
        return camera._comm.scan()

    def _open(self, port=None):

        if self._comm._ser.is_open :
            raise Exception("Camera is already opened!")

        self._comm.open(port)

        if self._comm._ser.is_open: 
            self.setDefaultParameters()

        return self

    def info(self):
        '''
        get camera information, such as model, firmware version, uid, resolution and serial port name.

        Returns
        ----------
        CameraInfo
            An instance of CameraInfo contains model, firmware version, uid, resolution and serial port name.
        '''

        chipType, chipVersion = self.getIdentification()
        model = "%d.%d" % (chipType, chipVersion)

        major, minor = self.getFirmwareRelease()
        firmware = "%d.%d" % (major, minor)

        waferId, chipId = self.getChipInformation()
        uid = "%02X%04X" % (waferId, chipId)

        return CameraInfo(model, firmware, uid, "160x60",  self._comm._ser.port)

    def close(self) :
        '''
        Close communication to the camera.
        '''

        self._comm.close()

    def setDefaultParameters(self) :
        '''
        Convenient method to set default parameters to control the ToF camera. You may set those parameters
        in your own application.
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

    def setModulationFrequency(self, frequency):
        '''
        Set Modulation Frequency, for wide view image, it has to be set to VALUE_20MHZ.
        '''
        self._comm.setModulationFrequency(frequency)

    def setModulationChannel(self, channel):
        '''
        Set Modulation Channel, for multiple cameras, you may set them work in different channels, 
        however if you have only one, set it to 0.
        '''
        self._comm.setModulationChannel(0, channel)

    def setMode(self, mode):
        '''
        Set camera mode. Currently supports wide view iamge only, which is 0.
        '''
        self._comm.setMode(mode)

    def setHdr(self, hdr):
        '''
        Set HDR mode. Currently not supported.
        '''
        self._comm.setHdr(hdr)

    def setIntegrationTime3d(self, index, t):
        '''
        Set Integration Time. 
        Integration Time could be from 0 to 1000, depends on the surface reflectivity and distance of the target object, 
        for an object in about 2-3 meters, you may try set it to 800.
        '''
        self._comm.setIntegrationTime3d(index, t)

    def setIntegrationTimeGrayscale(self, t):
        '''
        Set Integration Time for Grayscale. 
        If you request distance/depth plus grayscale image, you need set approriate “integration time grayscale”, 
        maximum allowed 25000, for example, regular in-door environment, set it to 8000.
        '''
        self._comm.setIntegrationTimeGrayscale(t)

    def setMinimalAmplitude(self, index, t):
        '''
        Set MinimalAmplitude. 
        MinimalAmplitude is the noise level minimum threshold, 
        for an object in about 2-3 meters in in-door environment, you may try set it to 60.
        '''
        self._comm.setMinimalAmplitude(index, t)

    def setOffset(self, offset):
        '''
        Set distance offset. 
        Normally this set it to 0.
        '''
        self._comm.setOffset(offset)

    def setRoi(self, x0, y0, x1, y1):
        '''
        Set ROI. 
        Currently not supported.
        '''
        self._comm.setRoi(x0, y0, x1, y1)

    @staticmethod
    def setColorMode(colorMode):
        '''
        Set ColorMode. 
        To use distance or grayscle for point cloud color.
        '''
        Camera._frameBuilder.setColorMode(colorMode)

    @staticmethod
    def setRange(z1, z2):
        '''
        Set Range. 
        To use distance for point cloud color, set the distance range.
        '''
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
        request Identification.
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
        To request raw data of a frame from camera.

        You may use readFrameRawData(frameType) only when you consider a two-step read-and-compose a Frame object, which readFrameRawData(frameType)
        to obtain a frame raw data, and then use FrameBuilder.composeFrame(dataArray, frameType) to create an Frame object, normally in
        a separate thread, to have a better frame rate.

        You may simply call readFrame(frameType) to obtain a Frame object without using this method if the frame rate is not critical.

        FrameType.DISTANCE: depth data only

        FrameType.DISTANCE_GRAYSCALE: depth data plus grayscale

        FrameType.DISTANCE_AMPLITUDE: depth data plus amplitude

        Returns
        ----------
        bytearray
            Length of the raw data will be different depends on the frameType specified:

        FrameType.DISTANCE: 2 bytes 32 float distance for each data point, 160 (image width) x 160 (image height) x 2;

        FrameType.DISTANCE_GRAYSCALE: 2 bytes 32 float distance and 1 byte unit 8 grayscale for each data point, 160 (image width) x 160 (image height) x (2 + 1);

        FrameType.DISTANCE_AMPLITUDE: 2 bytes 32 float distance and 2 bytes 32 float amplitude for each data point, 160 (image width) x 160 (image height) x (2 + 2);
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
        Convenient method to compose Frame using raw bytearray data.

        To compose a Frame object, you need to specify which FrameType of the raw data, which may be:

        FrameType.DISTANCE: distance / depth only

        FrameType.DISTANCE_GRAYSCALE: distance / depth plus grayscale

        FrameType.DISTANCE_AMPLITUDE: distance / depth plus amplitude

        Returns
        ----------
        Frame
            An instance of Frame.

            The members of the Frame object will be populated:
            
                data_depth,
                data_depth_rgb,
                points_3d

            In addition, depends on the FrameType requested, additional member may be populated:

            FrameType.DISTANCE_GRAYSCALE: data_grayscale.

            FrameType.DISTANCE_AMPLITUDE: data_amplitude.
        '''
        
        return Camera._frameBuilder.composeFrame(dataArray, frameType)

    def readFrame(self, frameType=FrameType.DISTANCE_GRAYSCALE) :
        '''
        A convenient method to directly get a new Frame object.

        Specifying a frameType to get a frame with distance / depth only, or distance / depth plus grayscale or amplitude:

        FrameType.DISTANCE: distance / depth only

        FrameType.DISTANCE_GRAYSCALE: distance / depth plus grayscale

        FrameType.DISTANCE_AMPLITUDE: distance / depth plus amplitude
        
        This method is an expensive call, alternatively you may use readFrameRawData and compose Frame from a separate thread in your application
        to get better frame rate.

        For example, for an application which the frame rate is not critical, a simple call of readFrame to get an instance of Frame object:

        frame = camera.readFrame(self, frameType=FrameType.DISTANCE)

        If your application require a fast frame rate, it might be a good idea to request frame raw data and compose Frame object in different threads:
        
        The local thread to request a frame raw data:

        dataArray = self.readFrameRawData(frameType)

        In another thread to compose the Frame object from dataArray, and the local thread can continue to request next frame raw data:

        _frameBuilder.composeFrame(dataArray, frameType)

        Returns
        ----------
        Frame
            An instance of Frame.

        The members of the Frame object will be populated:
            
                data_depth,
                data_depth_rgb,
                points_3d

            In addition, depends on the FrameType requested, additional member may be populated:

            FrameType.DISTANCE_GRAYSCALE: data_grayscale.

            FrameType.DISTANCE_AMPLITUDE: data_amplitude.

        Example of converting data_depth_rgb to OpenCV Mat object:
                
            mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
            mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

        Example of converting data_grayscale to OpenCV Mat object:
                
            mat_grayscale = np.frombuffer(frame.data_grayscale, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width)
            mat_grayscale = mat_grayscale.astype(np.uint8)

        Example of converting data_amplitude to OpenCV Mat object:

            mat_amplitude = np.frombuffer(frame.data_amplitude, dtype=np.float32, count=-1, offset=0).reshape(frame.height, frame.width)
            mat_amplitude = mat_amplitude.astype(np.uint8)
        '''
        
        dataArray = self.readFrameRawData(frameType)

        return Camera.composeFrame(dataArray, frameType)
