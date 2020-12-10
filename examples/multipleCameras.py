import numpy as np
import cv2

from TauLidarCommon.frame import FrameType
from TauLidarCamera.camera import Camera

def setup():
    cameras = []

    Camera.setRange(0, 4500)                   ## points in the distance range to be colored

    uiOffset = 20
    for port in Camera.scan():                 ## Scan for available Tau Camera devices
        camera = Camera.open(port)             ## Open the first available Tau Camera
        camera.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
        camera.setIntegrationTime3d(0, 1000)       ## set integration time 0: 1000
        camera.setMinimalAmplitude(0, 10)          ## set minimal amplitude 0: 80

        cameras.append(camera)


        cameraInfo = camera.info()

        print("\nToF camera opened successfully:")
        print("    model:      %s" % cameraInfo.model)
        print("    firmware:   %s" % cameraInfo.firmware)
        print("    uid:        %s" % cameraInfo.uid)
        print("    resolution: %s" % cameraInfo.resolution)
        print("    port:       %s" % cameraInfo.port)

        cv2.namedWindow('Tau %s'%cameraInfo.uid)
        cv2.moveWindow('Tau %s'%cameraInfo.uid, 20, uiOffset)
        uiOffset += 340

    print("\nPress Esc key over GUI or Ctrl-c in terminal to shutdown ...")  

    return cameras


def run(cameras):
    while True:
        for camera in cameras:
            frame = camera.readFrame(FrameType.DISTANCE)

            if frame: 
                mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
                mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

                # Upscalling the image
                upscale = 4
                img =  cv2.resize(mat_depth_rgb, (frame.width*upscale, frame.height*upscale))

                cv2.imshow('Tau %s'%camera.info().uid, img)

                if cv2.waitKey(1) == 27: break


def cleanup(cameras):
    print('\nShutting down ...')
    cv2.destroyAllWindows()
    for camera in cameras:
        camera.close()


if __name__ == "__main__":
    cameras = setup()

    try:
        run(cameras)
    except Exception as e:
        print(e)

    cleanup(cameras)






