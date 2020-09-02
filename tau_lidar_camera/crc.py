from .constants import *
from .util import *

POLYNOM = 0x04C11DB7
CRC_INIT_VALUE = 0xFFFFFFFF
XOR_VALUE = 0x00000000

def _calcCrc32Uint32(crc, data) :
    crc = crc ^ data
    for i in range(32) :
        if crc & 0x80000000 :
            crc = (crc << 1) ^ POLYNOM
        else :
            crc = crc << 1
    return(crc)

def _calcCrc32_32(data, size) :
    crc = CRC_INIT_VALUE
    for i in range(size) :
        crc = _calcCrc32Uint32(crc, data[i])
    return crc ^ XOR_VALUE

def calculateChecksum(data, size) :
    '''
    Calculate Checksum.

    Parameters
    ----------
    data : bytearray
        bytearray data.
    size : int
        size.
    '''
    return _calcCrc32_32(data, size)

def checksumIsCorrect(array, expectedSize) :
    '''
    Verify if the checksum is correct.

    Parameters
    ----------
    array : bytearray
        bytearray data.
    expectedSize : int
        expected size.
    '''
    ## The received CRC is the one in the data
    receivedCrc = getUint32LittleEndian(array, SIZE_HEADER + expectedSize)

    ## The wanted CRC is the one calculated out of the payload
    wantedCrc = calculateChecksum(array, SIZE_HEADER + expectedSize)

    byte0 = wantedCrc & 0xFF
    byte1 = (wantedCrc >> 8) & 0xFF
    byte2 = (wantedCrc >> 16) & 0xFF
    byte3 = (wantedCrc >> 24) & 0xFF
    wantedCrc_value = (byte3 << 24) | (byte2 << 16) | (byte1 << 8) | byte0

    if receivedCrc == wantedCrc_value :
        return True

    print("Checksum ERROR!!!")

    return False
