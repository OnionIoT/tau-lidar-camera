import os
import time

from TauLidarCommon.frame import FrameType
from TauLidarCamera.camera import Camera


delay = 0.2 #sec
outputDire = './samples'

def setup():
    camera = None
    ports = Camera.scan()                      ## Scan for available Tau Camera devices

    if len(ports) > 0:
        Camera.setRange(0, 4500)                   ## points in the distance range to be colored

        camera = Camera.open(ports[0])             ## Open the first available Tau Camera
        camera.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
        camera.setIntegrationTime3d(0, 1000)       ## set integration time 0: 1000
        camera.setMinimalAmplitude(0, 10)          ## set minimal amplitude 0: 80

        cameraInfo = camera.info()

        print("\nToF camera opened successfully:")
        print("    model:      %s" % cameraInfo.model)
        print("    firmware:   %s" % cameraInfo.firmware)
        print("    uid:        %s" % cameraInfo.uid)
        print("    resolution: %s" % cameraInfo.resolution)
        print("    port:       %s" % cameraInfo.port)

        print("\nPress Esc key over GUI or Ctrl-c in terminal to shutdown ...")
        
    return camera


def run(camera):

    count = 0

    if not os.path.exists(outputDire):
        os.makedirs(outputDire)

    print('Recording...')
    
    while True:
        frame = camera.readFrameRawData(FrameType.DISTANCE_AMPLITUDE)

        if frame:
            fName = '%s/%s.frame'%(outputDire, time.time())
            with open(fName, "wb") as binary_file: 
                binary_file.write(frame)
            print('\rFrame: %d'%count, end='')
            count += 1

        time.sleep(delay)

def cleanup(camera):
    print('\nShutting down ...')
    camera.close()


if __name__ == "__main__":
    camera = setup()

    if camera:
        try:
            run(camera)
        except Exception as e:
            print(e)

        cleanup(camera)
