import sys
import os
import asyncio
import json
from time import sleep, time
from threading import Thread, Lock

import numpy as np
import cv2

from TauLidarCommon.frame import FrameType, Frame
from TauLidarCamera.camera import Camera
from TauLidarCamera.constants import VALUE_10MHZ, VALUE_20MHZ
from TauLidarCommon.color import ColorMode

def main():
    attempts = 0
    while True:
        try:
            '''
            By default, Camera will connect to the first available ToF device. 
            Alternatively can specify serial port by using Camera.open('/dev/ttyACM0') to open specific port
            '''
            camera1 = Camera.open()

            cameraInfo = camera1.info()
            print("\nToF camera opened successfully:")

            print("    model:      %s" % cameraInfo.model)
            print("    firmware:   %s" % cameraInfo.firmware)
            print("    uid:        %s" % cameraInfo.uid)
            print("    resolution: %s" % cameraInfo.resolution)
            print("    port:       %s" % cameraInfo.port)

            camera1.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
            camera1.setIntegrationTime3d(0, 1000)        ## set integration time 0: 1000
            camera1.setMinimalAmplitude(0, 10)          ## set minimal amplitude 0: 80

            camera2 = Camera.open('/dev/cu.usbmodem3')

            cameraInfo = camera2.info()
            print("\nToF camera opened successfully:")

            print("    model:      %s" % cameraInfo.model)
            print("    firmware:   %s" % cameraInfo.firmware)
            print("    uid:        %s" % cameraInfo.uid)
            print("    resolution: %s" % cameraInfo.resolution)
            print("    port:       %s" % cameraInfo.port)

            camera2.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
            camera2.setIntegrationTime3d(0, 1000)        ## set integration time 0: 1000
            camera2.setMinimalAmplitude(0, 10)          ## set minimal amplitude 0: 80



            
            ## static
            Camera.setRange(0, 4500)                   ## points in the distance range to be colored
            
            break

        except Exception as e:
            attempts += 1

            if attempts > 10:
                print("Exiting due to failure of opening ToF camera!")
                print("Error: %s" % str(e))
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            sleep(5)
        sleep(0.1)


    print("\nPress Esc key over Depth Map or Grayscale to shutdown ...")  


    cv2.namedWindow('Tau %s'%camera1.info().uid)
    cv2.namedWindow('Tau %s'%camera2.info().uid)

    cv2.moveWindow('Tau %s'%camera1.info().uid, 20, 20)
    cv2.moveWindow('Tau %s'%camera2.info().uid, 20, 360)

    try:
        count = 0
        while True:

            for camera in [camera1, camera2]:
                frame = camera.readFrame(FrameType.DISTANCE)
                if frame == None: 
                    sleep(0.1)
                    continue

                count += 1

                mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
                mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

                # Upscalling the image
                upscale = 4
                img =  cv2.resize(mat_depth_rgb, (frame.width*upscale, frame.height*upscale))

                cv2.imshow('Tau %s'%camera.info().uid, img)


            if cv2.waitKey(1) == 27: break

    except KeyboardInterrupt:    
        print('\nShutting down ...')
        cv2.destroyAllWindows()
        sleep(0.1)
        camera.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main()
