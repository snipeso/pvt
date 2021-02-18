# PVT
This is an open source version of the Psychomotor Vigilance Task (PVT), a simple reaction time task, based on Basner et al. (2011).

### The task
Participants are presented with a red fixation rectangle. Every 2-10s, the rectangle is replaced with a rapidly increasing counter, and participants have to press a button as fast as possible. Their reaction time is presented for 1s, then the waiting period starts again. The whole task lasts 10 minutes. 

## Instructions

### Pre-requisites
This library relies only on [Psychopy](https://psychopy.org/).

Before running an experiment, look at the configurations in "./config/configPVT.py". Here, all the timings, and screen information and more are established. Adjust whatever you like.

#### Versions
This script has 3 versions, **main**, **demo**, and **debug**. The idea is you can set different combinations of settings for the different versions in the configurations file, then very quickly toggle between versions when running the task. If you want, you can add more versions. 

The idea is that "main" is for running the task. It has all the official timings, full screen display, and saves the output. "Demo" is a shorter version, that participants can use to try the task before starting. "Debug" opens a smaller window, and is used for software development.

### Steps
1. Open Psychopy, then run the script "MainPVT.py" to run the task. 
2. A popup will appear. Provide a participant ID, and session name (if applicable). Select a version.
3. Instructions on how to perform the task will appear. when ready, press spacebar.
4. Perform the task. While the instructions say to press "shift", any key except "q" will do. Ideally, use a USB button box to improve system reaction times.
5. If you want to quit early, press "q". 

### Output
The results are saved in "./output", in a subfolder defined as "{participant ID}_{session}". Each time you run the task, 2 ".log" files are produced. They can be read by anything, but the data inside is structured as a JSON. For an example on how to read this file, see the MATLAB example of "./read_output/importOutput.m". This function can be used to import the data as a table into MATLAB.

Both files include the same timestamp. This means that the files will never be overwritten by later tests. The file ending with "_configuration.log" contains all the information from the configurations used for that task.

The data JSON has the following entries:
- trialID: a sub-dictionary containing:
  - id: increasing numbers from 0
  - triggers: the number sent as a trigger to the EEG system. It starts from 192 so as not to interfere with smaller numbered triggers used in the task. When 255 is reached, two seperate triggers are sent.




### Setup


### Configurations




# Credits:

Design:

- Basner, M., & Dinges, D. F. (2011). Maximizing sensitivity of the psychomotor vigilance test (PVT) to sleep loss. Sleep, 34(5), 581-591.
