# Development Guide

This guide covers

* [Updating the Documentation](#updating-the-documentation)
* [Releasing a New Version of the Python Module](#releasing-a-new-version-of-the-python-module)
* [Local Development of the Package](#local-development-of-the-package)

## Updating the Documentation

The documentation on ReadTheDocs.io will be **automatically rebuilt and updated every time a push is made to the master branch**.

### Making Changes to the Documentation

The documentation can be found in the [`docs`](./docs/) directory. The documentation articles are written in [reStructuredText](https://devguide.python.org/documenting/) and the final result is generated using [Sphinx](https://www.sphinx-doc.org/en/master/).

See the [`docs/README.md`](./docs/README.md) for instructions on how to locally build and test the documentation.

## Releasing a New Version of the Python Module

A new version of the Python module will be **automatically released on PyPi when a new Release is made on GitHub**.

### Pre-requisites

* Update the version number in `TauLidarCamera/__version__.py`
* Create a Release in the GitHub Repo

### Versioning

Version numbers will follow the `MAJOR.MINOR.PATCH` syntax. More info [here](https://semver.org/).

### Release Notes

Each release must be accompanies with changelog notes outlining what's new. This includes:

* Features
* Bug fixes
* Performance improvements
* Etc

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
