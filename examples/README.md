# Examples

Samples of programs that use the Tau LiDAR Camera, each demonstrating the functionality of the TauLidarCamera Python module.

## `distance.py`

### What this demonstrates

The sample program demonstrates acquiring frames with distance / depth information only.

### Pre-requisites

Pre-requisites/dependencies:

  #### TauLidarCamera python module:

    #pip install TauLidarCamera

  #### OpenCV python module

    #pip install opencv-python


### How to Run

Command to run the program:

```    
#python distance.py
```

A new window rendering the 2D depth map will open:

![](../docs/img/example-distance-0.png)

## `distancePlusAmplitude.py`

### What this demonstrates

The sample program demonstrates acquiring frames with both distance / depth and amplitude image.

### Pre-requisites

Pre-requisites/dependencies:

  #### TauLidarCamera python module:

    #pip install TauLidarCamera

  #### OpenCV python module

    #pip install opencv-python

### How to Run

Command to run the program:

```    
#python distancePlusAmplitude.py
```

Two new windows will open to show the depth map and amplitude coming from the camera:

![](../docs/img/example-distance-amplitude-0.png)

## `distancePlusGrayscale.py`

### What this demonstrates

The sample program demonstrates acquiring frames with both distance / depth and grayscale image.

### Pre-requisites

Pre-requisites/dependencies:

  #### TauLidarCamera python module:

    #pip install TauLidarCamera

  #### OpenCV python module

    #pip install opencv-python

### How to Run

Command to run the program:

```
#python distancePlusGrayscale.py
```  

Two new windows will open to show the depth map and grayscale image coming from the camera:

![](../docs/img/example-distance-grayscale-0.png)

## `multipleCameras.py`

### What this demonstrates

Rendering depth data from **ALL connected** Tau Cameras in real-time. You are only limited by the number of USB ports!

### Pre-requisites

Pre-requisites/dependencies:

  #### TauLidarCamera python module:

    #pip install TauLidarCamera

  #### OpenCV python module

    #pip install opencv-python



### How to Run

Command to run the program:

```
#python multipleCameras.py
```  

A new window for each connected camera will open, showing the depth map coming from each:

![](../docs/img/example-multi-camera-0.png)
