import numpy as np
import cv2

from TauLidarCommon.frame import FrameType
from TauLidarCamera.camera import Camera

def setup():
    ports = Camera.scan()                      ## Scan for available Tau Camera devices

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


    cv2.namedWindow('Depth Map')
    cv2.namedWindow('Grayscale')

    cv2.moveWindow('Depth Map', 20, 20)
    cv2.moveWindow('Grayscale', 20, 360)

    return camera


def run(camera):
    while True:
        frame = camera.readFrame(FrameType.DISTANCE_GRAYSCALE)

        if frame: 
            mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
            mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

            mat_grayscale = np.frombuffer(frame.data_grayscale, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width)
            mat_grayscale = mat_grayscale.astype(np.uint8)

             # Upscalling the image
            upscale = 4
            depth_img =  cv2.resize(mat_depth_rgb, (frame.width*upscale, frame.height*upscale))
            grayscale_img =  cv2.resize(mat_grayscale, (frame.width*upscale, frame.height*upscale))

            cv2.imshow('Depth Map', depth_img)
            cv2.imshow('Grayscale', grayscale_img)

            if cv2.waitKey(1) == 27: break


def cleanup(camera):
    print('\nShutting down ...')
    cv2.destroyAllWindows()
    camera.close()


if __name__ == "__main__":
    camera = setup()

    try:
        run(camera)
    except Exception as e:
        print(e)

    cleanup(camera)





