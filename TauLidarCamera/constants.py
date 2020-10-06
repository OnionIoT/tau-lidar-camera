## Command format
COMMAND_SIZE_TOTAL    = 14                                  ## Cammand size total
COMMAND_SIZE_HEADER   = 4                                   ## Cammand header size
COMMAND_SIZE_CHECKSUM = 4                                   ## Cammand checksum size
COMMAND_SIZE_OVERHEAD = 8                                   ## COMMAND_SIZE_HEADER + COMMAND_SIZE_CHECKSUM
COMMAND_START_MARK    = 0xF5                                ## Command start marking
COMMAND_INDEX_COMMAND = 1                                   ## Cammand index
COMMAND_INDEX_DATA    = 2                                   ## Cammand payload data

## setup commands
COMMAND_SET_INTEGRATION_TIME_3D = 0x00                      ## Command to set the integration time for 3D operation
COMMAND_SET_INTEGRATION_TIME_GRAYSCALE = 0x01               ## Command to set the integration time for grayscale
COMMAND_SET_ROI = 0x02                                      ## Command to set the region of interest
COMMAND_SET_BINNING = 0x03                                  ## Command to set the binning
COMMAND_SET_MODE = 0x04                                     ## Command to set the mode
COMMAND_SET_MODULATION_FREQUENCY = 0x05                     ## Command to set the modulation frequency
COMMAND_SET_DLL_STEP = 0x06                                 ## Command to set the DLL step
COMMAND_SET_FILTER = 0x07                                   ## Command to set the filter parameters
COMMAND_SET_OFFSET = 0x08                                   ## Command to set the offset
COMMAND_SET_MINIMAL_AMPLITUDE = 0x09                        ## Command to set th minimal amplitude
COMMAND_SET_DCS_FILTER = 0x0A                               ## Command to set the DCS filter
COMMAND_SET_GAUSSIAN_FILTER = 0x0B                          ## Command to set the Gaussian filter
COMMAND_SET_FRAME_RATE = 0x0C                               ## Command to set/limit the frame rate
COMMAND_SET_HDR = 0x0D
COMMAND_SET_MODULATION_CHANNEL = 0x0E                       ## Command to set the modulation channel
COMMAND_SET_FILTER_SINGLE_SPOT = 0x0F                       ## Command to set the temporal filter for the single spot

## acquisition commands
COMMAND_GET_DISTANCE = 0x20                                 ## Command to request distance data
COMMAND_GET_AMPLITUDE = 0x21                                ## Command to request amplitude data
COMMAND_GET_DISTANCE_AMPLITUDE = 0x22                       ## Command to request distance and amplitude data
COMMAND_GET_DCS_DISTANCE_AMPLITUDE = 0x23                   ## Command to request distance, amplitude and DCS data at once
COMMAND_GET_GRAYSCALE = 0x24                                ## Command to request grayscale data
COMMAND_GET_DCS = 0x25                                      ## Command to request DCS data
COMMAND_SET_AUTO_ACQUISITION = 0x26                         ## Command to enable/disable the auto acquisition
COMMAND_GET_INTEGRATION_TIME_3D = 0x27                      ## Command to read the integration time. Important when using automatic mode
COMMAND_STOP_STREAM = 0x28                                  ## Command to stop the stream
COMMAND_GET_DISTANCE_GRAYSCALE = 0x29                       ## Command to request distance and grayscale

COMMAND_GET_IDENTIFICATION   = 0x47                         ## Command to identification
COMMAND_GET_CHIP_INFORMATION = 0x48                         ## Command to read the chip information
COMMAND_GET_FIRMWARE_RELEASE = 0x49                         ## Command to read the firmware release
COMMAND_GET_PRODUCTION_INFO  = 0x50                         ## Command to get the production info

## MODULATION
COMMAND_SET_MODULATION_FREQUENCY = 0x05
VALUE_10MHZ = 0 ## Value for 10MHz for command "COMMAND_SET_MODULATION_FREQUENCY"
VALUE_20MHZ = 1 ## Value for 20MHz for command "COMMAND_SET_MODULATION_FREQUENCY"

## 635 op mode
MODE_BEAM_A = 0                                             ## Normal operation with illumination beam A
MODE_BEAM_B_MANUAL = 1                                      ## Normal operation with illumination beam B (all settings by user, same as)
MODE_BEAM_B_RESULT = 2                                      ## Beam B with calibrated ROI, only one distance as result
MODE_BEAM_B_RESULT_DATA = 3                                 ## Beam B with calibrated ROI, one distance and the pixels as result
MODE_BEAM_AB_RESULT = 4                                     ## Beam A and B operating with calibrated ROI and only one distance as result
MODE_BEAM_AB_AUTO_RESULT = 5                                ## Beam A and B with automatic selection
MODE_BEAM_AB_INTERLEAVED_DATA = 6                           ## Beam A and B interleaved output

## Stream mode
SINGLE = 0                                                  ## Single frame mode
AUTO_REPEAT = 1                                             ## Auto repeat frame using same parameters
STREAM = 3                                                  ## Stream mode

## HDR
HDR_OFF = 0                                                 ## HDR off
HDR_SPATIAL = 1                                             ## Spatial HDR
HDR_TEMPORAL = 2                                            ## Temporal HDR

## IntegrationTime
INDEX_INDEX_3D = 2                                          ## Index of the integration time 3d index
INDEX_INTEGRATION_TIME_3D = 3                               ## Index of the integration time 3d

## AMPLITUDE
INDEX_INDEX_AMPLITUDE = 2                                   ## Index of the index
INDEX_AMPLITUDE = 3                                         ## Index of the minimal amplitude

## ROI
INDEX_ROI_X_MIN = 2                                         ## Index of ROI X MIN
INDEX_ROI_Y_MIN = 4                                         ## Index of ROI Y MIN
INDEX_ROI_X_MAX = 6                                         ## Index of ROI X MAX
INDEX_ROI_Y_MAX = 8                                         ## Index of ROI Y MAX

## Data format
DATA_START_MARK    = 0xFA                                   ## Data start marking
DATA_INDEX_LENGTH  = 2                                      ## Data length
DATA_INDEX_TYPE    = 1                                      ## Data type

## firmware returned data type
DATA_ACK = 0x00                                             ## Acknowledge from sensor to host
DATA_NACK = 0x01                                            ## Not acknowledge from sensor to host
DATA_IDENTIFICATION = 0x02                                  ## Identification to identify the device
DATA_DISTANCE = 0x03                                        ## Distance information
DATA_AMPLITUDE = 0x04                                       ## Amplitude information
DATA_DISTANCE_AMPLITUDE = 0x05                              ## Distance and amplitude information
DATA_GRAYSCALE = 0x06                                       ## Grayscale information
DATA_DCS = 0x07                                             ## DCS data
DATA_DCS_DISTANCE_AMPLITUDE = 0x08                          ## DCS, distance and amplitude all together
DATA_INTEGRATION_TIME = 0x09                                ## Integration time, answer to COMMAND_GET_INTEGRATION_TIME_3D
DATA_DISTANCE_GRAYSCALE = 0x0A                              ## Distance and grayscale data
DATA_LENS_CALIBRATION_DATA = 0xF7                           ## Lens calibration data
DATA_TRACE = 0xF8                                           ## Trace data
DATA_PRODUCTION_INFO = 0xF9                                 ## Production info
DATA_CALIBRATION_DATA = 0xFA                                ## Calibration data
DATA_REGISTER = 0xFB                                        ## Register data
DATA_TEMPERATURE = 0xFC                                     ## Temperature data
DATA_CHIP_INFORMATION = 0xFD                                ## Chip information data
DATA_FIRMWARE_RELEASE = 0xFE                                ## Firmware release
DATA_ERROR = 0xFF                                           ## Error number

## CHIP
MASK_CHIP_TYPE_DEVICE = 0x00FFFF00                          ## Chip information mask
SHIFT_CHIP_TYPE_DEVICE = 8                                  ## Chip information shift
CHIP_INFORMATION_DATA_SIZE = 4                              ## Chip information data size

## IDENTITY
DATA_IDENTIFICATION = 0x02
DATA_FIRMWARE_RELEASE = 0xFE
IDENTIFICATION_DATA_SIZE = 4                                ## Chip information data size
INDEX_WAFER_ID = 6
INDEX_CHIP_ID = 4

## Firmware release
FIRMWARE_RELEASE_DATA_SIZE = 4                              ## Chip information data size
MASK_VERSION = 0x000000FF
SHIFT_VERSION = 0

## TOF 635 image
TOF_635_IMAGE_HEADER_SIZE  = 80                            ## 635 IMAGE HEADER SIZE
