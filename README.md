# Human Version of the Paired Associate Learning (PAL) Task with Event Outputs, Non-invasive Audio-Visual Stimulation, and VR Support
This Python-based version of the Paired Associate Learning (PAL) task has been redeveloped to integrate with the DAQ system for sending signals. The task remains identical to the online CANTAB PAL task, allowing you to experience the task with non-invasive audio-video stimulation and VR support.

## Features
* Non-invasive stimulation: Includes both audio and video stimulation, as well as combinations (audio + video).
* Event Outputs: Integration with a DAQ system for sending signals based on task events.
* VR Support: Compatible with VR setups to enhance the immersive experience.
* Python-based: Developed in Python using the PsychoPy framework for experimental control.

# Installation
## Install Anaconda
Download and install Anaconda to manage your environment and dependencies.
* Import Environment from the psychopy-env.yml
After installing Anaconda, create a new environment using the provided psychopy-env.yml file.
* Installing NIDAQmx for Python
To interface with the National Instruments DAQ, install the NIDAQmx library:

## For Python:
Run the following command in your terminal or command prompt:

bash
Copy
Edit
python -m pip install nidaqmx
If using PsychoPy, close all sessions, open the command prompt with admin privileges, navigate to the PsychoPy installation folder, and then run the command above.

## For Conda:
You can also install it using Conda from the conda-forge channel:

bash
Copy
Edit
conda install -c conda-forge nidaqmx-python

## Requirements
* Fast Computer: Tested on a laptop with a 10th generation i9 processor.
* High Refresh Rate Screen: Tested with an Alienware screen with 480Hz refresh rate and HTC Vive Pro2 (90Hz) VR headset.
* Good Quality Headphones: Tested with AudioTechnica M50x wired headphones.
* National Instruments NIDAQ 6001: Required for hardware interaction with the DAQ.


## Steps to Run
-Go to the Protocol Folder: Open the folder containing the protocol and configuration files.

-Edit Stimulation Time Values in the Protocol folder:

* StimNum: The stimulus number (just a number).
* Stim_Type: Type of stimulation. Options include:
** A: Audio
** V: Video
** VA: Video + Audio
** MVA: Movie + Video + Audio
* Stim_Duration: Duration of the stimulation in seconds.
* Stim_VisPrimaryFreq: Set to half of the screen refresh rate (e.g., 4Hz, 40Hz).
* Stim_VisSecondaryFreq: Set to half of the screen refresh rate (e.g., 4Hz, 40Hz).
* Stim_VisFreqStyle: Choose between pure sin waves or isochrones (both tested).
* Stim_AudPrimaryFreq: Audio frequency (must be lower than half the sampling frequency).
* Stim_AudSecondaryFreq: Audio secondary frequency (must be lower than half the sampling frequency).
* Stim_AudFc: Audio carrier frequency (e.g., 100Hz, 250Hz).
* Stim_AudFreqStyle: Choose between pure sin waves or isochrones (both tested).
* Stim_AudModulation: Choose modulation type (AM or FM).
* Stim_VisAudOffset: Set the delay between video and audio.
* Stim_MovieName: If playing a movie, specify the filename.
* Stim_AudioVolume: Set the audio volume.
* Stim_RectangleOpacity: Set the maximum opacity for visual stimulation/intensity.
* Stim_RectSize: Set the field of view size.
* Stim_MovieSize: Set the size of the video.
* Stim_MovieOpacity: Set the opacity of the movie.
* PAL_task: Specify whether the task is a PAL task or not.
* ConditionName: Choose between Eye Open (EO) or Eye Closed (EC).
* SubName: Name of the file.
* DataFileNum: File number for data tracking.

-Edit Sequence Order:
* Open the seq.txt file and arrange the stimulation order. The StimNum values will be read and executed in sequence. Multiple sequences can be executed one after another.

Run the Task:
Execute the task by running the Python script that interfaces with PsychoPy and the DAQ system to manage stimulation.

Data Output:
All stimulation data and task parameters are saved in the data folder. The file structure will include:

Event logs in EventList (see HardwareAndSoftwareResources/EventLists.docx for details).
Notes
Make sure all hardware (DAQ, VR headset, screen, headphones) is connected and functioning before running the task.
The sequence configuration allows flexibility in stimulation ordering, and multiple sequences can be run in succession.
Ensure the PsychoPy environment is set up correctly with all necessary libraries installed for smooth operation.
Enjoy the immersive experience of the PAL task with non-invasive stimulation and VR support!
