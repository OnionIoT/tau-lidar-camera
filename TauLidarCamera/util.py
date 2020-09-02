def setUint32LittleEndian(buffer, index, value) :
    '''
    set Uint32 Little Endian.

    Parameters
    ----------
    buffer : bytearray
        data array.
    index : int
        starting index.
    value : int
        value to be set.
    '''
    buffer[index] = value & 0xFF
    buffer[index+1] = (value >> 8) & 0xFF
    buffer[index+2] = (value >> 16) & 0xFF
    buffer[index+3] = (value >> 24) & 0xFF

def setUint16LittleEndian(buffer, index, value) :
    '''
    set Uint16 Little Endian.

    Parameters
    ----------
    buffer : bytearray
        data array.
    index : int
        starting index.
    value : int
        value to be set.
    '''
    buffer[index] = value & 0xFF
    buffer[index+1] = (value >> 8) & 0xFF

def setInt16LittleEndian(buffer, index, value) :
    '''
    set Int16 Little Endian.

    Parameters
    ----------
    buffer : bytearray
        data array.
    index : int
        starting index.
    value : int
        value to be set.
    '''
    buffer[index] = value & 0xFF
    buffer[index+1] = (value >> 8) & 0xFF

def getUint32LittleEndian(array, index) :
    '''
    get Uint32 Little Endian.

    Parameters
    ----------
    array : bytearray
        data array.
    index : int
        starting index.
    '''
    byte0 = array[index]
    byte1 = array[index+1]
    byte2 = array[index+2]
    byte3 = array[index+3]
    value = (byte3 << 24) | (byte2 << 16) | (byte1 << 8) | byte0
    return value

def getUint16LittleEndian(array, index) :
    '''
    get Uint16 Little Endian.

    Parameters
    ----------
    array : bytearray
        data array.
    index : int
        starting index.
    '''
    byte0 = array[index]
    byte1 = array[index+1]
    value = (byte1 << 8) | byte0
    return value

def getValueLsb(value) :
    '''
    get Lsb value.

    Parameters
    ----------
    value : int
        masked value.
    '''
    return (value & 0xFFFF)

def getValueMsb(value) :
    '''
    get Msb value.

    Parameters
    ----------
    value : int
        masked value.
    '''
    return (value >> 16)
