Quickstart
==========

To get started in a hurry, follow the examples on this page.

First, make sure the TauLidarCamera module is `installed <install>`_

Imports:
--------

Before you start, you need import some TauLiDar libraries:

   from TauLidarCommon.frame import FrameType, Frame

   from TauLidarCamera.camera import Camera

   from TauLidarCamera.constants import VALUE_20MHZ

   from TauLidarCommon.color import ColorMode


Open Camera:
------------
Call static method of Camera to open an instance:

   camera = Camera.open()

Query camera info:
------------------
You may verify if the camera connected correctly by checking the camera info:

   cameraInfo = camera.info()

   print("\nToF camera opened successfully:")

   print("    model:      %s" % cameraInfo.model)

   print("    firmware:   %s" % cameraInfo.firmware)

   print("    uid:        %s" % cameraInfo.uid)

   print("    resolution: %s" % cameraInfo.resolution)

   print("    port:       %s" % cameraInfo.port)

Set parameters:
---------------
For multiple cameras, you may set them work on different channels, however if you have only one, set it to 0:

   camera.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0

Integration Time could be from 0 to 1000, depends on the reflectibility and distance of the target object, for an object in about 2-3 meters, you may try set it to 800:

   camera.setIntegrationTime3d(0, 800)        ## set integration time 0: 1000

Noise level (Minimal Amplitude):

   camera.setMinimalAmplitude(0, 60)          ## set minimal amplitude 0: 80

Distance range (mm)  to be colored:

   Camera.setRange(0, 4500)                   ## points in the distance range to be colored
   
If you request distance/depth plus grayscle image, you need set approriate "integration time grayscale":

   camera.setIntegrationTimeGrayscale(15000)  ## set integration time grayscale: 8000, needed when requiring FrameType.DISTANCE_GRAYSCALE

Read a frame:
-------------

You may request a frame with distance/depth data only, or distance/depth plus grayscle image, or distance/depth plus amplitude image.

To request a frame with distance/depth data only:

   frame = camera.readFrame(FrameType.DISTANCE)
   
To request a frame with distance/depth plus grayscle image:

   frame = camera.readFrame(FrameType.DISTANCE_GRAYSCALE)
   
To request a frame with distance/depth plus grayscle image:

   frame = camera.readFrame(FrameType.DISTANCE_AMPLITUDE)

Display depth map using OpenCV:
-------------------------------

To display depth map, convert the data array of depth data to 3 channel BGR image:

   mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)

   mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

   cv2.imshow('Depth Map', mat_depth_rgb)

If you see a window displaying depth map, congratulation, your Tau LiDAR camera is working!

If you requested distance/depth plus grayscle image, to display the grayscle image, convert the data array of depth data to single channel image:

   mat_grayscale = np.frombuffer(frame.data_grayscale, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width)
   
   mat_grayscale = mat_grayscale.astype(np.uint8)

If you requested distance/depth plus grayscle image, to display the grayscle image, convert the data array of depth data to single channel image:

   mat_amplitude = np.frombuffer(frame.data_amplitude, dtype=np.float32, count=-1, offset=0).reshape(frame.height, frame.width)
   
   mat_amplitude = mat_amplitude.astype(np.uint8)


   
   


