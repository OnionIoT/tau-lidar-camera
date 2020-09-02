
class CameraInfo :
    '''
    Camera Information.
    
    Attributes
    ----------
    model: 
        Camera model.
    firmware: 
        Firmware version.
    uid: 
        Camera identification.
    resolution:
        Camera resolution
    port: 
        Serial port
    '''
    def __init__(self, _model, _firmware, _uid, _resolution, _port) :
        self.model      = _model
        self.firmware   = _firmware
        self.uid        = _uid
        self.resolution = _resolution
        self.port       = _port
