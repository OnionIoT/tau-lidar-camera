Troubleshooting
==================

A few troubleshooting tips in case you encounter any issues!

Bad frame ignored error -> Need a better cable
-----------------------------------------------

**The Problem:**

If you run a program that uses the TauLidarCamera library and it successfully opens to camera, but then shows an error that looks something like this:

.. code-block:: bash

    Data error, actual size: 35644, expected size: 38480
    Bad frame ignored, bytes length: 35564
    Bad frame ignored, bytes length: 0
    Bad frame ignored, bytes length: 0
    ...


**The Solution:**

Try switching to a **high-quality cable**! If possible, try using a not-super-long USB-C to USB-C cable from a reputable brand. Then try running the program again.

Try to avoid:

* Long cables
* USB hubs
* USB adapters

Try to use:

* Shorter cables
* Direct USB-C to USB-C if possible
* Cables from reputable brands
