Installation
====================================

Here we'll cover how to install TauLidarCamera. You need to make sure it's installed correctly before you can dive into using it!

Prerequisite: Install Python
----------------------------

Self-explanatory: you will need to have Python installed!

Download and install Python at https://www.python.org/downloads/.
**Make sure you install version 3.7 or higher**.

If you have questions about using Python, check out the `official Python.org  instructions <https://docs.python.org/3/using/index.html>`_.

$ python -m pip install TauLidarCamera
--------------------------------------

To install TauLidarCamera, you can use pip and run this command in your terminal of choice::

    $ python -m pip install TauLidarCamera

Alternate Method: Get the Source Code
-------------------------------------

TauLidarCamera is developed on `GitHub <https://github.com/OnionIoT/tau-lidar-camera>`_

You can either clone the public repository::


    $ git clone git@github.com:OnionIoT/tau-lidar-camera.git


Or, download a zip of the repo::

    $ curl -OL https://github.com/OnionIoT/tau-lidar-camera/archive/master.zip

Once you have a copy of the source, you can embed it in your own Python package, or install it into your site-packages::

    $ cd tau-lidar-camera
    $ python -m pip install .
