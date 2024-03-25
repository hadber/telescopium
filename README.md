# telescopium

In order to install, please do the following:

First, we create a virtual environment:
```
python -m venv tele-venv
```

Then we activate it with
```
source ./tele-venv/bin/activate
```

And then install all of our requirements:
```
pip install -r requirements.txt
```

Using is as simple as running the following:
```
python main.py
```

In order to install dearpygui on a raspberrypi, please refer to the following guide:
https://github.com/hoffstadt/DearPyGui/issues/1741

It should, eventually, be supported on a pi out of the box - but, until then, please check out the aformentioned link


Make sure of the following two things: 
- in raspi-config, camera legacy support is disabled
- also in raspi-config, under advanced options -> GL Driver that you have G1 Legacy enabled.

Also, in order to use the "still" configuration with the HQ camera, you will need to increase the cma size in /boot/config.txt, relevant info here:
https://github.com/raspberrypi/picamera2/issues/422

It will only run by doing: `LIBGL_ALWAYS_SOFTWARE=true python main.py`
