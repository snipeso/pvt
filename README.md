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

#### Configurations
The pre-defined configurations, saved in "./config/configPVT.py", are set up to used immediately. If you wish to adjust any parameters, feel free to do so, they will be saved as part of the output.

Many configurations have 3 options, one for each version. The idea is that you can adjust the combination of settings to your preference.

There are extra features that can be activated:
- A reminder to answer a questionnaire at the end of the task can be played.
- Triggers can be selectively sent to a BrainAmp EEG system, and/or Pupil Labs eyetracker.


### Steps
1. Open Psychopy, then run the script "MainPVT.py" to run the task. 
2. A popup will appear. Provide a participant ID, and session name (if applicable). Select a version.
3. Instructions on how to perform the task will appear. when ready, press spacebar.
4. There is a brief waiting period. This is to give participants time to settle down and get ready. 
5. Perform the task. While the instructions say to press "shift", any key except "q" will do. Ideally, use a USB button box to improve system reaction times.
6. If you want to quit early, press "q".

### Output
The results are saved in "./output", in a subfolder defined as "{participant ID}_{session}". Each time you run the task, 2 ".log" files are produced, one is the JSON of the configurations used, the other is a more detailed log of everything that happens during the task. The main results are saved in a ".csv" file. All have the same root filename, which includes a timestamp so that it's not possible to overwrite pre-existing files, even if you use the same participant and session names.



# Credits:

Design:

- Basner, M., & Dinges, D. F. (2011). Maximizing sensitivity of the psychomotor vigilance test (PVT) to sleep loss. Sleep, 34(5), 581-591.
