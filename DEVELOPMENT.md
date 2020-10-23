# Development Guide

## Local Development of the Package

> Will use [Virtual Environments](https://docs.python.org/3/tutorial/venv.html) and [PIP Editable Installs](https://pip.pypa.io/en/latest/reference/pip_install/#editable-installs) to locally install the package for development purposes

In your testing directory, setup the virtual environment **(only needs to be done once)**:
```
python3 -m venv .
```

Activate virtual environment:
```
source bin/activate
```

Local install of the [tau-lidar-common](https://github.com/OnionIoT/tau-lidar-common) package:
```
python -m pip install -e /path/to/tau-lidar-common
```

Local install of the tau-lidar-camera package:
```
python -m pip install -e /path/to/tau-lidar-camera
```

Now run your testing program.

**Any edits to the `tau-lidar-camera` package source code in `/path/to/tau-lidar-camera` will be reflected when the testing program is run again**
