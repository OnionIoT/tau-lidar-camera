import os
import time

import numpy as np
import cv2

from TauLidarCommon.frame import FrameType
from TauLidarCamera.camera import Camera

def setup():
    Camera.setRange(0, 4500)

    print("\nPress Esc key over GUI or Ctrl-c in terminal to shutdown ...")

    cv2.namedWindow('Depth Map')
    cv2.namedWindow('Amplitude')

    cv2.moveWindow('Depth Map', 20, 20)
    cv2.moveWindow('Amplitude', 20, 360)


def run(framesDir):
    delay = 0.1 #sec

    fileList = os.listdir(framesDir)
    fileList.sort()

    for filename in fileList:
        if not '.frame' in filename: continue

        print (filename)

        with open(os.path.join(framesDir, filename), 'rb') as f: 
            dataArray = bytearray(f.read())

            frame = Camera.composeFrame(dataArray, FrameType.DISTANCE_AMPLITUDE)

            if frame:
                mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
                mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

                mat_amplitude = np.frombuffer(frame.data_amplitude, dtype=np.float32, count=-1, offset=0).reshape(frame.height, frame.width)
                mat_amplitude = mat_amplitude.astype(np.uint8)

                # Upscalling the image
                upscale = 4
                depth_img =  cv2.resize(mat_depth_rgb, (frame.width*upscale, frame.height*upscale))
                amplitude_img =  cv2.resize(mat_amplitude, (frame.width*upscale, frame.height*upscale))

                cv2.imshow('Depth Map', depth_img)
                cv2.imshow('Amplitude', amplitude_img)

                if cv2.waitKey(1) == 27: break
        time.sleep(delay)

            



if __name__ == "__main__":
    setup()
    
    framesDir = 'samples'

    if os.path.exists(framesDir):
        try:
            print("\nPress Esc key over GUI or Ctrl-c in terminal to shutdown ...")
            run(framesDir)
        except Exception as e:
            print(e)
