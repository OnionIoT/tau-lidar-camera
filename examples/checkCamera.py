import argparse
import numpy as np
import cv2

from TauLidarCommon.frame import FrameType
from TauLidarCamera.camera import Camera

def scanPortsAndSetup():
    camera = None

    ports = Camera.scan()                      ## Scan for available Tau Camera devices
    print('\nFound %d possible device(s)'%len(ports))

    for port in ports:
        print('Attempting to connect to device on port \'%s\''%port)
        camera = setup(port)

    return camera

def setup(port):
    camera = None

    Camera.setRange(0, 4500)                   ## points in the distance range to be colored

    camera = Camera.open(port)             ## Open the first available Tau Camera
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
    while True:
        frame = camera.readFrame(FrameType.DISTANCE)

        if frame:
            mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
            mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

            # Upscalling the image
            upscale = 4
            img =  cv2.resize(mat_depth_rgb, (frame.width*upscale, frame.height*upscale))

            cv2.imshow('Depth Map', img)

            if cv2.waitKey(1) == 27: break


def cleanup(camera):
    print('\nShutting down ...')
    cv2.destroyAllWindows()
    camera.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Try connecting to any available Tau LiDAR Camera.\nIf no port argument is specified scan all serial ports will be scanned.')
    parser.add_argument('--port', metavar='<serial port>', default=None,
                        help='Specify a serial port instead of trying all available Tau LiDAR Cameras')
    args = parser.parse_args()

    port = args.port

    if port is None:
        camera = scanPortsAndSetup()
    else:
        print('Attempting to connect to device on port \'%s\''%port)
        camera = setup(port)

    if camera:
        try:
            run(camera)
        except Exception as e:
            print(e)

        cleanup(camera)
