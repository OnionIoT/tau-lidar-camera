import os
import time
from signal import signal, SIGINT

from TauLidarCommon.frame import FrameType
from TauLidarCamera.camera import Camera


outputDir = './samples'
runLoop = True

def setup():
    camera = None
    ports = Camera.scan()                      ## Scan for available Tau Camera devices

    if len(ports) > 0:
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

        print("\nPress Ctrl-c in terminal to shutdown ...")

    return camera


def run(camera):
    global runLoop
    count = 0

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    print('Recording...')

    while runLoop:
        frame = camera.readFrameRawData(FrameType.DISTANCE_AMPLITUDE)

        if frame:
            fName = '%s/%s.frame'%(outputDir, time.time())
            with open(fName, "wb") as binary_file:
                binary_file.write(frame)
            print('\rFrame: %d'%count, end='')
            count += 1

def cleanup(camera):
    print('\nShutting down ...')
    camera.close()

def handler(signal_received, frame):
    global runLoop
    runLoop = False


if __name__ == "__main__":
    camera = setup()
    signal(SIGINT, handler)

    if camera:
        try:
            run(camera)
        except Exception as e:
            print(e)

        cleanup(camera)
