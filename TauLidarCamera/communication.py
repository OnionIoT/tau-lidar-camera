import serial
import serial.tools.list_ports
from time import sleep
import binascii

from .constants import *
from .crc import *
from .util import *

class Communication:
    '''
    Communication to the ToF sensor via serial port.

    Attributes
    ----------

    Methods
    -------
    open(_port)
        To open the communication to ToF sensor.
    close()
        To close the communication to ToF sensor.

    setModulationFrequency(frequency)
        set Modulation Frequency (10mHz or 10mHz).
    setModulationChannel(autoChannelEnabled, channel)
        set Modulation Channel.
    setMode(mode)
        set Mode.
    setHdr(hdr)
        set Hdr.
    setIntegrationTimeGrayscale(integrationTime)
        set Integration Time Grayscale.
    setOffset(offset)
        set Offset.
    setIntegrationTime3d(index, integrationTime)
        set Integration Time 3d.
    setMinimalAmplitude(index, amplitude)
        set Minimal Amplitude.
    setRoi(xMin, yMin, xMax, yMax)
        set Roi.

    getChipInformation()
        get Chip Information.
    getFirmwareRelease()
        get Firmware Release.
    getDistanceGrayscale()
        get Distance Grayscale.
    '''

    def __init__(self):
        self._ser = serial.Serial()
        self._ser.baudrate = 4000000
        self._ser.timeout = 0.001
        self._ser.parity = serial.PARITY_NONE
        self._ser.stopbits = serial.STOPBITS_ONE
        self._ser.bytesize = serial.EIGHTBITS

    def open(self, port):
        '''
        auto detect sensor at serial port and open communication to the sensor if port is not given,
        or open communication to specific serial port.

        Parameters
        ----------
        port: str
            serial port the sensor connected.
        '''
        if self._ser.is_open :
            raise Exception("Serial port is already opened!")

        message = ""
        if port is None:
            print('Looking for connected Tau LiDAR Camera hardware ...')
            ports = list(serial.tools.list_ports.comports())
            connected = False
            for port_no, description, address in ports:
                try:
                    self._ser.port = port_no
                    self._ser.open()

                    ## Verify if it is valid device
                    dataArray = self.getIdentification()
                    identificationValue = int(binascii.hexlify(dataArray), 16)
                    chipType = (identificationValue & MASK_CHIP_TYPE_DEVICE) >> SHIFT_CHIP_TYPE_DEVICE
                    chipVersion = (identificationValue & MASK_VERSION) >> SHIFT_VERSION

                    nChipType = int(chipType)
                    nChipVersion = int(chipVersion)

                    if (nChipType >= 4 and nChipVersion >= 0):
                        connected = True
                        break
                except:
                    self._ser.close()

            if not connected:
                message = "No Tau Camera found, please check: \n1. If Tau Camera is connected; \n2. If current user has permission to access all serial ports."
                raise Exception(message)
        else:
            self._ser.port = port
            try:
                self._ser.open()
            except:
                message = "Failed connecting to the serial port %s, please check: \n1. If Tau Camera is connected; \n2. If current user has permission to access the port" % port
                raise Exception(message)

        return self

    def close(self):
        '''
        close communication to the sensor.
        '''
        if self._ser.is_open :
            self._ser.close()

    def _write(self, data):

        if not self._ser.is_open :
            print("ERROR: serial port is not open!")
            return

        data[0] = COMMAND_START_MARK
        checksum = calculateChecksum(data, (COMMAND_SIZE_TOTAL - 4))

        setUint32LittleEndian(data, (COMMAND_SIZE_TOTAL - 4), checksum)

        ################################
        ##debeg_str= "SEND COMMAND: "
        ##for i in range(14) :
        ##    buf = "%x" % data[i]
        ##    debeg_str += buf
        ##print(debeg_str)
        ################################

        return self._ser.write(data)

    def _read(self, size):

        if not self._ser.is_open :
            print("ERROR: serial port is not open!")
            return

        size_with_command = size + 8

        array = bytearray(0)
        count = 0
        while (len(array) < size_with_command) :
            len_pending = size_with_command - len(array)
            in_waiting = self._ser.in_waiting
            sz = min(len_pending, self._ser.in_waiting)
            if sz > 0 :
                buf = self._ser.read(sz)
                a = bytearray(buf)
                array.extend(a)
            else :
                sleep(0.0001)

            count += 1
            if count > 1000 : break

        return self._processData(array, size)

    def _processData(self, array, size):

        data_length = len(array)

        if data_length == 0 :
            print("      DATA ERROR - length is 0")
            #return False
            return (-1, bytearray(0))

        ## Check for the start mark
        if (array[0] != DATA_START_MARK) :
            #print("      DATA ERROR - the start byte is not DATA_START_MARK")
            #return True
            return (-1, bytearray(0))

        if data_length < COMMAND_SIZE_HEADER :
            #print("      DATA ERROR - length shorter than COMMAND_SIZE_HEADER")
            #return True
            return (-1, bytearray(0))

        ## Cancel here if not enough bytes received
        if data_length < COMMAND_SIZE_OVERHEAD :
            #print("      DATA ERROR - length shorter than COMMAND_SIZE_OVERHEAD")
            #return True
            return (-1, bytearray(0))

        ## Get the expexted size
        expectedSize = self._getExpextedSize(array)

        #if checksumIsCorrect(array, expectedSize) : ## calculate checksum for a frame data size 28880 is too time consumming, turn off checking for now
        type = self._getType(array)
        dataArray = array
        dataArray[0:COMMAND_SIZE_HEADER] = []

        ## Remove checksum at the end
        dataArray[expectedSize:expectedSize + COMMAND_SIZE_CHECKSUM] = []

        ## Remove the rest at the end
        dataArray[expectedSize:len(dataArray)] = []

        data_length = len(dataArray)

        if (data_length < size):
            print("Data error, actual size: %d, expected size: %d" % (data_length, size))

        return (type, dataArray)

    def _sendCommand(self, data, size):

        if self._write(data) > 0:
            return self._read(size)

        return None

    def _sendCommandWithoutData(self, command, size):

        data = bytearray(14)
        data[1] = command
        return self._sendCommand(data, size)

    def _sendCommandSingleByte(self, command, payload, size):
        data = bytearray(COMMAND_SIZE_TOTAL)

        ## Add the command
        data[COMMAND_INDEX_COMMAND] = command

        ## Add the single byte at the first position
        data[COMMAND_INDEX_DATA] = payload

        return self._sendCommand(data, size)

    def _sendCommand2xByte(self, command, payload0, payload1, type):
        data = bytearray(COMMAND_SIZE_TOTAL)

        ## Add the command
        data[COMMAND_INDEX_COMMAND] = command

        ## Add the first byte
        data[COMMAND_INDEX_DATA] = payload0

        ## Add the second byte
        data[COMMAND_INDEX_DATA + 1] = payload1

        return self._sendCommand(data, type)

    def _sendCommandUint16(self, command, payload, size):
        data = bytearray(COMMAND_SIZE_TOTAL)

        ## Add the command
        data[COMMAND_INDEX_COMMAND] = command

        ## Add the payload
        setUint16LittleEndian(data, COMMAND_INDEX_DATA, payload)

        return self._sendCommand(data, size)

    def _sendCommandInt16(self, command, payload, size):
        data = bytearray(COMMAND_SIZE_TOTAL)

        ## Add the command
        data[COMMAND_INDEX_COMMAND] = command

        ## Add the payload
        setInt16LittleEndian(data, COMMAND_INDEX_DATA, payload)

        return self._sendCommand(data, size)

    def _getExpextedSize(self, array):
        return getUint16LittleEndian(array, DATA_INDEX_LENGTH)

    def _getType(self, array) :
        return array[DATA_INDEX_TYPE]

    def setModulationFrequency(self, frequency):
        '''
        set Modulation Frequency.

        Parameters
        ----------
        frequency
            VALUE_10MHZ (10mHz) or VALUE_20MHZ (20mHz).
        '''
        return self._sendCommandSingleByte(COMMAND_SET_MODULATION_FREQUENCY, frequency, 0) ## expected data length: 0

    def setModulationChannel(self, autoChannelEnabled, channel):
        '''
        set Modulation Channel.

        Parameters
        ----------
        autoChannelEnabled
            on or off the auto Channel
        channel
            0 - 10.
        '''
        return self._sendCommand2xByte(COMMAND_SET_MODULATION_CHANNEL, autoChannelEnabled, channel, DATA_ACK)

    def setMode(self, mode):
        '''
        set Mode.

        Parameters
        ----------
        mode
            0 - wide FOV
        '''
        return self._sendCommandSingleByte(COMMAND_SET_MODE, mode, 0) ## expected data length: 0

    def setHdr(self, hdr):
        '''
        set HDR.

        Parameters
        ----------
        hdr
            0 - HDR Off
        '''
        self._hdr = hdr

        return self._sendCommandSingleByte(COMMAND_SET_HDR,  hdr, 0)  ## expected data length: 0

    def setIntegrationTimeGrayscale(self, integrationTime):
        '''
        set Integration Time Grayscale.

        Parameters
        ----------
        integrationTime
            0 - 50000
        '''
        return self._sendCommandUint16(COMMAND_SET_INTEGRATION_TIME_GRAYSCALE, integrationTime, 0)

    def setOffset(self, offset):
        '''
        set Offset.

        Parameters
        ----------
        offset
            distance offset
        '''
        return self._sendCommandInt16(COMMAND_SET_OFFSET, offset, 0)  ## expected data length: 0

    def setIntegrationTime3d(self, index, integrationTime):
        '''
        set set Integration Time 3d.

        Parameters
        ----------
        index
            integrationTime index
        integrationTime
            integrationTime
        '''
        data = bytearray(COMMAND_SIZE_TOTAL)

        ## Add the command
        data[COMMAND_INDEX_COMMAND] = COMMAND_SET_INTEGRATION_TIME_3D

        ## Add the index
        data[INDEX_INDEX_3D] = index

        ## Add the time
        setUint16LittleEndian(data, INDEX_INTEGRATION_TIME_3D, integrationTime)

        return self._sendCommand(data, 0)

    def setMinimalAmplitude(self, index, amplitude):
        '''
        set Minimal Amplitude.

        Parameters
        ----------
        index
            MinimalAmplitude index
        amplitude
            amplitude
        '''
        data = bytearray(COMMAND_SIZE_TOTAL)

        ## Add the command
        data[COMMAND_INDEX_COMMAND] = COMMAND_SET_MINIMAL_AMPLITUDE

        ## Add the index
        data[INDEX_INDEX_AMPLITUDE] = index

        ## Add the amplitude
        setUint16LittleEndian(data, INDEX_AMPLITUDE, amplitude)

        return self._sendCommand(data, 0)

    def setRoi(self, xMin, yMin, xMax, yMax):
        '''
        set Roi.

        Parameters
        ----------
        xMin
            xMin
        yMin
            yMin
        xMax
            xMax
        yMax
            yMax
        '''
        data = bytearray(COMMAND_SIZE_TOTAL + 4 * 2) ## 4 two-bytes data (uint16_t in c++)

        ## Add the command
        data[COMMAND_INDEX_COMMAND] = COMMAND_SET_ROI

        ## xMin
        setUint16LittleEndian(data, INDEX_ROI_X_MIN, xMin)

        ## yMin
        setUint16LittleEndian(data, INDEX_ROI_Y_MIN, yMin)

        ## xMax
        setUint16LittleEndian(data, INDEX_ROI_X_MAX, xMax)

        ## yMax
        setUint16LittleEndian(data, INDEX_ROI_Y_MAX, yMax)

        self._xMin = xMin
        self._yMin = yMin
        self._xMax = xMax
        self._yMax = yMax

        return self._sendCommand(data, 0)

    def getChipInformation(self):
        '''
        get Chip Information.
        '''
        type, data = self._sendCommandWithoutData(COMMAND_GET_CHIP_INFORMATION, CHIP_INFORMATION_DATA_SIZE)
        return data

    def getIdentification(self):
        '''
        get getIdentification.
        '''
        type, data = self._sendCommandWithoutData(COMMAND_GET_IDENTIFICATION, IDENTIFICATION_DATA_SIZE)
        return data

    def getFirmwareRelease(self):
        '''
        get Firmware Release.
        '''
        type, data = self._sendCommandWithoutData(COMMAND_GET_FIRMWARE_RELEASE, FIRMWARE_RELEASE_DATA_SIZE)
        return data

    def getDistanceGrayscale(self):
        '''
        get Distance Grayscale image.
        '''
        dataSize = 0

        if self._hdr == HDR_SPATIAL : dataSize = 3 * (self._xMax - self._xMin + 1) * (self._yMax - self._yMin + 1) / 2 + 80 ## 16 bit distance/2 + 8 bit grayscale/2
        else :
            dataSize = 3 * (self._xMax - self._xMin + 1) * (self._yMax - self._yMin + 1) + 80 ## 16 bit distance + 8 bit grayscale;

        type, data = self._sendCommandSingleByte(COMMAND_GET_DISTANCE_GRAYSCALE, AUTO_REPEAT, dataSize)
        return data

    def getDistanceAmplitude(self):
        '''
        get Distance Amplitude image.
        '''
        dataSize = 0

        if self._hdr == HDR_SPATIAL : dataSize = 2 * (self._xMax - self._xMin + 1) * (self._yMax - self._yMin + 1) + 80 ## 16 bit distance/2 + 16 bit
        else :
            dataSize = 4 * (self._xMax - self._xMin + 1) * (self._yMax - self._yMin + 1) + 80 ## 16 bit distance + 16 bit amplitude

        type, data = self._sendCommandSingleByte(COMMAND_GET_DISTANCE_AMPLITUDE, AUTO_REPEAT, dataSize)
        return data

    def getDistance(self):
        '''
        get Distance only.
        '''
        dataSize = 0

        if self._hdr == HDR_SPATIAL : dataSize = (self._xMax - self._xMin + 1) * (self._yMax - self._yMin + 1) + 80 ## 16 bit distance
        else :
            dataSize = 2 * (self._xMax - self._xMin + 1) * (self._yMax - self._yMin + 1) + 80 ## 16 bit distance

        type, data = self._sendCommandSingleByte(COMMAND_GET_DISTANCE, AUTO_REPEAT, dataSize)
        return data
