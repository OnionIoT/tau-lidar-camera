Quickstart
==========

To get started in a hurry, follow the examples on this page.

First, make sure the TauLidarCamera module is `installed <install>`_

Imports:
-------

   from TauLidarCommon.frame import FrameType, Frame
   
   from TauLidarCamera.camera import Camera
   
   from TauLidarCamera.constants import VALUE_20MHZ
   
   from TauLidarCommon.color import ColorMode
   

Open Camera:
-----------

   camera = Camera.open()
   
Query camera info:
-----------------

   cameraInfo = camera.info()
   
   print("\nToF camera opened successfully:")

   print("    model:      %s" % cameraInfo.model)
   
   print("    firmware:   %s" % cameraInfo.firmware)
   
   print("    uid:        %s" % cameraInfo.uid)
   
   print("    resolution: %s" % cameraInfo.resolution)
   
   print("    port:       %s" % cameraInfo.port)
   
Set parameters:
--------------

   camera.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
   
   camera.setIntegrationTime3d(0, 800)        ## set integration time 0: 1000
   
   camera.setMinimalAmplitude(0, 60)          ## set minimal amplitude 0: 80

   Camera.setRange(0, 4500)                   ## points in the distance range to be colored

Read a frame:
------------

   frame = camera.readFrame(FrameType.DISTANCE)

Display depth map using OpenCV:
------------------------------

   mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
   
   mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

   cv2.imshow('Depth Map', mat_depth_rgb)

   cv2.waitKey(0)

Examples
--------

For samples of complete programs that use the Tau LiDAR Camera, see the `Example Programs in the GitHub repo <https://github.com/OnionIoT/tau-lidar-camera/tree/master/examples>`_
