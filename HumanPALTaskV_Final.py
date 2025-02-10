## Human PAL Task Development

#07/04/2023
#Avoir la random task et ne pas avoir a chnage rde fichier pour les stimulationavec film


#Import Files
from __future__ import absolute_import, division
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import csv
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import random  as rand

import os  # handy system and path functions
import sys  # to get file system encoding
import pandas as pd

from psychopy.hardware import keyboard
import glob
import ReadProtocolFiles, CreateAllObjects
import nidaqmx
from nidaqmx.constants import (LineGrouping)

import AccessoryFun

## Setup Directories
# Change low latency high priority audio output
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '4'
visual.useFBO = True  # if available (try without for comparison)
core.rush(True, realtime=True)

expName = 'Stimulation_and_PALTask'  # from the Builder filename that created this script

expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
okayokay = {'What kind of EEG are you using ? wet/dry': ''}
dlg = gui.DlgFromDict(dictionary=okayokay, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel




system = nidaqmx.system.System.local()
nDevices=[]
for device in system.devices:
    nDevices.append(device.name=='NI6001')

Device_NI6001_Exists=any(nDevices)
if not Device_NI6001_Exists:
    mydlg=gui.Dlg(title='Device not found!')
    mydlg.addText('NI 6001 Device is not found. The events will not be sent. Press "OK" to continue without sending the events or press "cancel" to abort the Experiement.')
    ok_data=mydlg.show()
    if mydlg.OK==False:
        core.quit()

TypeEEG = okayokay['What kind of EEG are you using ? wet/dry']
expInfo['expName'] = expName
expInfo['psychopyVersion'] = 'psychopyVersion 22.1.0'
SubjectName=expInfo['participant']

DryEvent = []

core.wait(0.1)

if TypeEEG == 'dry':
    AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
else:
    AccessoryFun.SendSignals(Device_NI6001_Exists,100,core)
DryEvent.append(100)
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
Date=data.getDateStr(format='%Y%m%d')  # add a simple timestamp

DataFolderPath=_thisDir + os.sep + 'data'+os.sep+'%s_%s_%s' % (Date, SubjectName, expName)#+os.sep+'Data_%s' % (expInfo['session'])
if not os.path.exists(DataFolderPath):
    os.mkdir(DataFolderPath)
    
DataFolderPath=_thisDir + os.sep + 'data'+os.sep+'%s_%s_%s' % (Date, SubjectName, expName)+os.sep+'Data_%s' % (expInfo['session'])

if not os.path.exists(DataFolderPath):
    os.mkdir(DataFolderPath)


#Read Protocol File and get Current Data
CurrentStimParams, PAL2Execute, TargetLocations=ReadProtocolFiles.GetAllDataFiles()



# After Changing the directory to current folder load the function files
frameTolerance = 0.001  # how close to onset before 'same' frame
FrameN = -1 #set initial frame number to -1
#ReinforcementDuration=0.5
ReinforcementDuration=1


# create some flags for expereiment

endExpNow = False  # flag for 'escape' or other condition => quit the exp



# Setup the Window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=1, winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=(-1,-1,-1), depthBits=24,  colorSpace='rgb', blendMode='avg',multiSample =True,numSamples =1, useFBO=False, units='norm')

MonitorRefreshRate=round(win.getActualFrameRate()) #Get Monitor refreshrate
MonitorFrameProp=[[0]*6]*MonitorRefreshRate*3600 #initialize 1 hr for Screen Properties



# Create all Objects
Movie01, RectBox, Aud01, Cross, Distractors, CorrectTargets, TargetLocations, CorrectTargetLocs, AudSignal = CreateAllObjects.CreateObjects(win)



# Initialize mouse and Keyboard
mouse = event.Mouse()
defaultKeyboard = keyboard.Keyboard()



# Create Some Timers
globalClock = core.Clock()  # to track the time since experiment started
trialClock = core.Clock()
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine
subRoutineTimer=core.CountdownTimer(0)
RevealTimer = core.Clock()

_timeToFirstFrame = win.getFutureFlipTime(clock="now")
trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip

# TrialData.loc=pd.DataFrame({"TrialNumber": None, 
#                  "NumChoices":None,
#                  "CorrectImageNames": None,
#                  "DistractorRevealOrder": None,
#                  "CorrectImageLocations": None,
#                  "ITI":None ,
#                  "ReinforcementDuration":None,
#                  "TrialStartTime": None,
#                  "DistractorOpenTimes":None,
#                  "DistractorCloseTimes":None,
#                  "CorrectImageOnsetTime": None,
#                  "ChoiceSelected":None,
#                  "SelectionTime":None,
#                  "IsChoiceSelectedCorrect": None,
#                  "TrialCompleted": None})
TrialData=pd.DataFrame(data=None)

# Get List of images and set time for reveal
ImageList = np.stack(glob.glob('.\\Images\\*.bmp'))  # Get Stored Image list
T4reveal=PAL2Execute.PAL_SampDisplayDuration[0]
# Get Correct Targets
Images4Trial=np.random.choice(len(ImageList), PAL2Execute.PAL_TotalStims[0], replace=False)
CorrectTargets=[]
CorrectTargetLocs=np.random.choice(len(TargetLocations), PAL2Execute.PAL_TotalStims[0], replace=False) # Randomly assign location of the correct target
Count_NumTargets=0 # this is just to have unique name of the component in the compnnent array
for stim in range(PAL2Execute.PAL_TotalStims[0]):
    CorrectTargets.append(visual.ImageStim(win=win, name='CorrectTar'+str(Count_NumTargets), image=ImageList[Images4Trial[stim]], mask=None, ori=0.0, pos=(TargetLocations[CorrectTargetLocs[stim]][0]*.75,TargetLocations[CorrectTargetLocs[stim]][1]*.75), size=(0.3, 0.3), color=[1,1,1], colorSpace='rgb', opacity=1, flipHoriz=False,units='norm', flipVert=False, texRes=128.0, interpolate=True, depth=0.0))
    Count_NumTargets+=1

if CurrentStimParams.PAL_task==-1:
    TimesExecuted=range(1)
else: 
    TimesExecuted=range(PAL2Execute.PAL_TrialRepeats[0])


if CurrentStimParams.PAL_task==-1:
    TimesExecuted=range(1)
else: 
    TimesExecuted=range(10)


random_task =[20,20,20,20,20,21,21,21,21,21]
np.random.shuffle(random_task)
print(random_task)
## Start the trial
for TrialNumber in TimesExecuted:
    #input('Press enter to continue')
    
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    if CurrentStimParams.PAL_task!=-1:
        #define Files Location
        ProtocolFilelocation='.\\Protocols\\Protocol.xls'
        PALFileLocation='.\\Protocols\\PALTask.xlsx'
    
        Protocol= pd.read_excel(ProtocolFilelocation, sheet_name="Protocol1")
    
        # Get Current Task to execute
        
        CurrentTask= random_task[TrialNumber]
        # read the PAL task to execute for the current Stim
        CurrentStimParams=Protocol.iloc[CurrentTask]
        PAL2Execute= pd.read_excel(PALFileLocation, sheet_name=CurrentStimParams.PAL_task)
    
    subRoutineTimer.reset(PAL2Execute.PAL_Timeout[0]) # Reset the timeout timer for the subroutine (Time to wait before timeouting the trial in absense of response)
    t0=RevealTimer.getTime()
    Images4Trial=np.random.choice(len(ImageList), PAL2Execute.PAL_TotalStims[0], replace=False)
    
        
    #Get distractor reveal order This changes in each trial
    DistractorRevealOrder=linspace(0,len(Distractors)-1 ,len(Distractors),dtype='int', endpoint=True) # Create a linear array for indexes of DIstractrors
    shuffle(DistractorRevealOrder) #Shuffle distractor order
    
    
    # CorrectTargets=[]
    CorrectTargetLocs=np.random.choice(len(TargetLocations), PAL2Execute.PAL_TotalStims[0], replace=False) # Randomly assign location of the correct target
    Count_NumTargets=0
    for CorrectTargetN in CorrectTargets: 
        CorrectTargetN.image=ImageList[Images4Trial[Count_NumTargets]]
        CorrectTargetN.pos=(-2,-2)
        Count_NumTargets+=1
        
        
   #  # this is just to have unique name of the component in the compnnent array
    # for stim in range(PAL2Execute.PAL_TotalStims[0]):
    #     CorrectTargets.append(visual.ImageStim(win=win, name='CorrectTar'+str(Count_NumTargets), image=ImageList[Images4Trial[stim]], mask=None, ori=0.0, pos=(TargetLocations[CorrectTargetLocs[stim]][0]*.75,TargetLocations[CorrectTargetLocs[stim]][1]*.75), size=(0.4, 0.4), color=[1,1,1], colorSpace='rgb', opacity=1, flipHoriz=False,units='norm', flipVert=False, texRes=128.0, interpolate=True, depth=0.0))
    #     
    
   
    count_DistractorOrder=0
    
    # Initialize flags for the  current Trial
    displayall=True
    isSamplePhaseCompleted=False
    isChoicePhaseCompleted=False
    CurrentChoiceSelected=0
    ContinueTrial=True 
    isClicked=True
    ChoicePhaseCorrect=[]
    executeTrialOnset=True
    SampleShown=0
    DistractorOpenTimesAll=[]
    DistractorCloseTimesAll=[]
    ChoicesSelectedAll=[]
    ChoiceSelectedTime=[]
    ChoiceSelectedCorrect=[]
    StimOnsetTime=[]
    
    #Change opacity to match the one as specified in protocol file
    RectBox.opacity=CurrentStimParams.Stim_RectangleOpacity   
    if CurrentStimParams.PAL_task!=-1:
        if CurrentTask == 20:
            if TypeEEG == 'dry':
                AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
            else:
                AccessoryFun.SendSignals(Device_NI6001_Exists,110,core)
            DryEvent.append(110)
            
        if CurrentTask == 21:
            if TypeEEG == 'dry':
                AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
            else:
                AccessoryFun.SendSignals(Device_NI6001_Exists,220,core)
            DryEvent.append(220)

        


    TrialInfo=pd.DataFrame({"TrialNumber": TrialNumber, 
                     "NumChoices":PAL2Execute.PAL_TotalStims[0],
                     "CorrectImageNames": [Images4Trial],
                     "DistractorRevealOrder": [DistractorRevealOrder],
                     "CorrectImageLocations": [CorrectTargetLocs],
                     "ITI":round(rand.uniform(PAL2Execute.PAL_ITIMin[0],PAL2Execute.PAL_ITIMax[0]),2) ,
                     "ReinforcementDuration":ReinforcementDuration,
                     "TrialStartTime": globalClock.getTime(),
                     "DryEvent":None,
                     "DistractorOpenTimes":None,
                     "DistractorCloseTimes":None,
                     "CorrectImageOnsetTime": None,
                     "ChoiceSelected":None,
                     "SelectionTime":None,
                     "IsChoiceSelectedCorrect": None,
                     "TrialCompleted": None})
          
    t_FirstFlip= win.getFutureFlipTime(clock=None) # Get time of screen update
    ## Run the main routine 
    while subRoutineTimer.getTime()>0 and ContinueTrial:
        
        # test for escape key to quit the task
        if defaultKeyboard.getKeys(keyList=["escape"]):
            if TypeEEG == 'dry':
                AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
            else:
                AccessoryFun.SendSignals(Device_NI6001_Exists,102,core)
            DryEvent.append(102)
            Aud01.stop()
            TrialInfo.DistractorOpenTimes =[DistractorOpenTimesAll]
            TrialInfo.DistractorCloseTimes=[DistractorCloseTimesAll]
            AccessoryFun.SaveLogFiles(TrialData, MonitorFrameProp, AudSignal, FrameN, DataFolderPath)
       
            win.close()
            core.quit()
        
                
        tThisFlipGlobal = win.getFutureFlipTime(clock=None) # Get time of screen update
       
        # if executeTrialOnsetreset and (abs(sin(tThisFlipGlobal)) >0.01):
        #     continue
        # else: 
        #     executeTrialOnsetreset=False
       
        FrameN +=1 # Increment frame number
        
        if FrameN==0: # If the frame number is 0 ie the first frame start all the components except for distractors and correct targets
            if not (CurrentStimParams.Stim_MovieName == -1):
                if 'M' in CurrentStimParams.Stim_Type:
                    Movie01.opacity=CurrentStimParams.Stim_MovieOpacity
                else:
                    Movie01.opacity=0
                Movie01.setAutoDraw(True)
            Aud01.play(loops=3600, when=win)
            RectBox.setAutoDraw(True)
            Cross.setAutoDraw(True)
            
            
        if executeTrialOnset:
          
                
            for CorrectTargetN in CorrectTargets:
                CorrectTargetN.setAutoDraw(True)
            for DistractorN in Distractors:
                DistractorN.opacity=1
                DistractorN.setAutoDraw(True)
            executeTrialOnsetreset=False
           
        if not(CurrentStimParams.Stim_VisSecondaryFreq==-1):
            offset_Primary=-np.pi/4  #3*np.pi/4
            offset_Secondary=0
            dfactor=2;
        else:
            offset_Primary=np.pi
            offset_Secondary=0
            dfactor=1
            
            
             
         # Visual Stimulation
        if 'V' in CurrentStimParams.Stim_Type:
       
            PrimarySinWave = np.sin(2 * np.pi * CurrentStimParams.Stim_VisPrimaryFreq/dfactor * (tThisFlipGlobal-t_FirstFlip)+offset_Primary) #make primary sine wave
            if CurrentStimParams.Stim_VisFreqStyle == "Isochrone":
                PrimarySinWave = PrimarySinWave > 0
            if CurrentStimParams.Stim_VisSecondaryFreq > 0: # if nested frequency is specified
                SecondarySinWave = np.sin(2 * np.pi * CurrentStimParams.Stim_VisSecondaryFreq*(tThisFlipGlobal-t_FirstFlip)+offset_Secondary) #secondary sin wave if nested frequency is specified
            else:
                SecondarySinWave = 1 #secondary sine wave is unity
            if CurrentStimParams.Stim_VisFreqStyle == "Isochrone":
                SecondarySinWave = SecondarySinWave > 0
    
            if CurrentStimParams.Stim_VisFreqStyle == "Isochrone":
                VisualSignal2 = ((PrimarySinWave * SecondarySinWave)-.5)*2 #If isochrone rescale between -1 and 1
            else:
                VisualSignal2 = PrimarySinWave * SecondarySinWave
            del (PrimarySinWave, SecondarySinWave)  
             
            RectBox.color=(0, 0, 0)+VisualSignal2 #VisualSignal[frameN] #Change rectangle color in gray range as specified by visual signal
            RectBox.opacity=CurrentStimParams.Stim_RectangleOpacity   #Change opacity to match the one as specified in protocol file
            

         
      
            
        #RUN PAL TASK     
        if not CurrentStimParams.PAL_task==-1:
            idx=0
            if not isSamplePhaseCompleted: 
                if RevealTimer.getTime()-t0>T4reveal: # if the time has elapsed depending on the previous state decide to deisplay all or a small subset
                    t0=RevealTimer.getTime()
                  
                    #  all distractors are sequentially hidden and closed
                    if count_DistractorOrder == len(DistractorRevealOrder):
                        isSamplePhaseCompleted=True #once all disstarctors are shown 
                    if not displayall:
                        DistractorCloseTimesAll.append(globalClock.getTime())
                        # =DistractorRevealOrder[count_DistractorOrder]
                        if TypeEEG == 'dry':
                            AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
                        else:
                            AccessoryFun.SendSignals(Device_NI6001_Exists,32+count_DistractorOrder,core)
                        DryEvent.append(32+count_DistractorOrder)
                        count_DistractorOrder+=1  
                    else: 
                        #ok =DistractorRevealOrder[count_DistractorOrder]
                        if TypeEEG == 'dry':
                            AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
                        else:
                            AccessoryFun.SendSignals(Device_NI6001_Exists,48+count_DistractorOrder,core)
                        DryEvent.append(48+count_DistractorOrder)
                        # DistractorRevealOrder[count_DistractorOrder]
                        DistractorOpenTimesAll.append(globalClock.getTime())
                        
                    displayall=not displayall #flag to switch to unhiding one distactor 
                else: 
                    if displayall:
                        for CorrectTargetN in CorrectTargets:
                            CorrectTargetN.pos=(-2,-2)
                            CorrectTargetN.draw()
                            #Make all distractors opaque
                        for DistractorN in Distractors:
                            DistractorN.opacity=1 
                            DistractorN.draw()
                    else:
                       
                        for CurrStim2disp in (CorrectTargetLocs):
                            if DistractorRevealOrder[count_DistractorOrder]==CurrStim2disp:
                               CorLoc=CorrectTargetLocs==DistractorRevealOrder[count_DistractorOrder]
                               updateidx=[i for i, x in enumerate(CorLoc) if x]
                               CorrectTargets[updateidx[0]].pos=(TargetLocations[CurrStim2disp][0]*.75,TargetLocations[CurrStim2disp][1]*.75)
                               idx+=1
                        
                        # for CorrectTargetN in CorrectTargets:
                        #     CorrectTargetN.draw()
                            #Make all distractors opaque
                        for DistractorN in Distractors:
                            DistractorN.opacity=1 
                            
                            
                        Distractors[DistractorRevealOrder[count_DistractorOrder]].opacity =0 # hide one distractor box
                        for DistractorN in Distractors:
                            DistractorN.draw()
                           
            if not isChoicePhaseCompleted and isSamplePhaseCompleted:
                CorrectTargetOriginalPosition=(-2,-2)
                CorrectTargets[CurrentChoiceSelected].pos=(0,0)
                currentDistractor=-1
                if isClicked:
                    StimOnsetTime.append(globalClock.getTime())
                    isClicked=False
                for DistractorN in Distractors:
                    currentDistractor+=1
                    if mouse.isPressedIn(DistractorN):
                        isClicked=True
                        ok = int(np.where(DistractorRevealOrder == CorrectTargetLocs[CurrentChoiceSelected])[0])
                     
                        if TypeEEG == 'dry':
                            AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
                        else:
                            AccessoryFun.SendSignals(Device_NI6001_Exists,64+ok,core)
                        DryEvent.append(64+ok)
                        SelectedDistractor=currentDistractor
                        CorrectTargets[CurrentChoiceSelected].pos=CorrectTargetOriginalPosition
                        CorrectTargets[CurrentChoiceSelected].draw()
                        ChoicesSelectedAll.append(currentDistractor);
                        ChoiceSelectedTime.append(globalClock.getTime())
                        win.flip() 
                        if currentDistractor==CorrectTargetLocs[CurrentChoiceSelected]:
                            
                            TargetCorrect=True
                            ChoiceSelectedCorrect.append(1)
                           
                            
                            Distractors[SelectedDistractor].lineColor=(-1,1,-1)
                            Distractors[SelectedDistractor].draw()
                            
                            win.flip()
                            if TypeEEG == 'dry':
                                AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
                            else:
                                AccessoryFun.SendSignals(Device_NI6001_Exists,119,core)
                            DryEvent.append(119)
                        

                            core.wait(ReinforcementDuration)
                            
                            Distractors[SelectedDistractor].lineColor=(-1,-1,-1)
                            Distractors[SelectedDistractor].draw()
                            win.flip()
                            CurrentChoiceSelected+=1
                            
                            if CurrentChoiceSelected==PAL2Execute.PAL_TotalStims[0]:
                                for CorrectTargetN in CorrectTargets:
                                    CorrectTargetN.setAutoDraw(False)       
                                    win.flip() 
                                if TypeEEG == 'dry':
                                    AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
                                else:
                                    AccessoryFun.SendSignals(Device_NI6001_Exists,121,core)
                                DryEvent.append(121)

                                core.wait(TrialInfo.ITI[0]-ReinforcementDuration) #apply ITI
                                TrialInfo.TrialCompleted=globalClock.getTime()
                                ContinueTrial=False
                        

                        else: 
                            
                            TargetCorrect=False
                            ChoiceSelectedCorrect.append(0)
                            
                            Distractors[SelectedDistractor].lineColor=(1,-1,-1)
                            Distractors[SelectedDistractor].draw()
                            
                            win.flip()
                            if TypeEEG == 'dry':
                                AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
                            else:
                                AccessoryFun.SendSignals(Device_NI6001_Exists,120,core)
                            DryEvent.append(120)
                            
                            
                            
                            Distractors[SelectedDistractor].lineColor=(-1,-1,-1)
                            Distractors[SelectedDistractor].draw()
                            win.flip()
                            CurrentChoiceSelected+=1
                            core.wait(ReinforcementDuration)
                            if CurrentChoiceSelected==PAL2Execute.PAL_TotalStims[0]:
                                for CorrectTargetN in CorrectTargets:
                                    CorrectTargetN.setAutoDraw(False)       
                                    win.flip() 
                                if TypeEEG == 'dry':
                                    AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
                                else:
                                    AccessoryFun.SendSignals(Device_NI6001_Exists,121,core)
                                DryEvent.append(121)
                        
                                core.wait(TrialInfo.ITI[0]-ReinforcementDuration) #apply ITI
                                TrialInfo.TrialCompleted=globalClock.getTime()
                                ContinueTrial=False
                
                            
                            """"
                            core.wait(TrialInfo.ITI[0]-ReinforcementDuration) #apply ITI
                            Distractors[SelectedDistractor].lineColor=(-1,-1,-1)
                            Distractors[SelectedDistractor].draw()
                            win.flip()
                            #isChoicePhaseCompleted=True
                            TrialInfo.TrialCompleted=globalClock.getTime()
                           #ContinueTrial=False
                            """
                
        else: 
            for nDist in Distractors: 
                #nDist.image=ImageList[Images4Trial[Count_NumTargets]]
                nDist.pos=(-2,-2)
                #Count_NumTargets+=1
        
        if  (CurrentStimParams.PAL_task==-1): 
            if (globalClock.getTime()-TrialInfo.TrialStartTime[0])>CurrentStimParams.Stim_Duration:
                ContinueTrial=False
            
            
        win.flip(clearBuffer=True)
        MonitorFrameProp[FrameN]=[FrameN,round(tThisFlipGlobal,4), RectBox.opacity,round(RectBox.fillColor[0],2), round(RectBox.fillColor[1],2), round(RectBox.fillColor[2],2) ]
      
    if ContinueTrial==False:
        TrialInfo.DistractorOpenTimes =[DistractorOpenTimesAll]
        TrialInfo.DistractorCloseTimes=[DistractorCloseTimesAll]
        TrialInfo.IsChoiceSelectedCorrect=[ChoiceSelectedCorrect]
        TrialInfo.ChoiceSelected=[ChoicesSelectedAll]
        TrialInfo.SelectionTime= [ChoiceSelectedTime]
        TrialInfo.CorrectImageOnsetTime=[StimOnsetTime]
        TrialInfo.DryEvent = [DryEvent]
        TrialData=pd.concat([TrialData, TrialInfo])

win.flip() #Final flip before ending experiment

CurrSeqFile = open("seq.txt", "r+")
CurrentTask = int(CurrSeqFile.readline())
CurrSeqFile.close()

new_file = open("seq.txt", "w+")
new_file.write("")
new_file.write(str((CurrentTask)+1)) # remove comment
new_file.close()

# # Close win and quit core

AccessoryFun.SaveLogFiles(TrialData, MonitorFrameProp, AudSignal, FrameN, DataFolderPath)

         
if TypeEEG == 'dry':
    AccessoryFun.SendSignals(Device_NI6001_Exists,1,core)# Task started
else:
    AccessoryFun.SendSignals(Device_NI6001_Exists,101,core)
DryEvent.append(101)
TrialData.to_csv('your_name.csv', header = True, index=False)
Aud01.stop()

win.close()        

core.quit()
