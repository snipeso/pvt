# pvt

# Install env

1. `pyvenv env` to create env
2. `source env/bin/activate` to enter env
3. `pip install -r requirements.txt` (run over and over until no more errors)

### alternatively, install env for all projects:

1. `cp -r hemi-pvt/env/ psychopyEnv`
2. `pyvenv psychopyEnv/`
3. `source psychopyEnv/bin/activate`

# create requirements:

1. `pip freeze > requirements.txt`

## install psychopy after error:

1. `sudo apt install python3-dev libx11-dev libasound2-dev portaudio19-dev libusb-1.0-0-dev libxi-dev build-essential libgtk-3-dev gtk3.0 python3-wxgtk3.0`
2. maybe necessary but probably not: `sudo apt-get install libjpeg-dev libtiff-dev libgtk2.0-dev libsdl1.2-dev freeglut3 freeglut3-dev libnotify-dev libgstreamerd-3-dev`

## get access to port for triggers

- add your user to the right group:
  - `sudo usermod -a -G dialout $USER`
- identify the name of the port, and save as "serial_device" in CONF
  - in terminal, do `ls /dev/tty{USB,ACM}*`, should be just 1

## Todo

- make counter font size cm dependent

## Eventual TODOs

- Provide results
- check that the task is as described in paper
- testing git

# External resources

Sounds:

- horn.wav: https://freesound.org/people/mcpable/sounds/131930/
- design: Basner, M., & Dinges, D. F. (2011). Maximizing sensitivity of the psychomotor vigilance test (PVT) to sleep loss. Sleep, 34(5), 581-591.
