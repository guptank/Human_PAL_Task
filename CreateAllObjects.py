def CreateObjects(win):
    #from __future__ import absolute_import, division
    from psychopy import locale_setup
    from psychopy import prefs
    from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
    from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                    STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

    import numpy as np  # whole numpy lib is available, prepend 'np.'
    from numpy import (sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray)
    from numpy.random import random, randint, normal, shuffle, choice as randchoice
    import os  # handy system and path functions
    import sys  # to get file system encoding
    import pandas as pd

    from psychopy.hardware import keyboard
    import glob


    import ReadProtocolFiles


    CurrentStimParams, PAL2Execute, TargetLocations=ReadProtocolFiles.GetAllDataFiles()

    # CurrentStimParams.Stim_AudPrimaryFreq=-1
    # CurrentStimParams.Stim_MovieName=-1


    #remove
    #win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, winType='pyglet', allowGUI=False, allowStencil=False, monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb', blendMode='avg',multiSample =False, useFBO=True, units='norm')


    #assign Movie filenames
    if CurrentStimParams.Stim_MovieName==-1:
        VideoFile='.\MediaResources\BlankVideo.mp4'
    else:
        VideoFile='.\MediaResources\Video'+ str(CurrentStimParams.Stim_MovieName)+'.mp4'

    Phas1 = -np.pi / 2 #For making sure that the phases are correctly aligned
    fs = int(44100) # Define Audio Frequency
    T4Audio = np.linspace(0, CurrentStimParams.Stim_Duration, fs * CurrentStimParams.Stim_Duration, endpoint=True) #Audio stim timings



    if CurrentStimParams.Stim_AudPrimaryFreq==-1:
        # Define Parameters

        AudSignal=np.sin(2 * np.pi * 0 * T4Audio) # Create a blank signal
    else:
          modulation_index = 1  # ALWAYS CONSTANT! Assuming 100% modulation
          A_c = 1  # Amplitudes are fixed for carrier and mod
          A_m = 1
          if CurrentStimParams.Stim_AudModulation == 'AM':  # AM
              if CurrentStimParams.Stim_AudFreqStyle == 'Isochrone':
                  PrimarySinWaveAud = np.sin(2 * np.pi * CurrentStimParams.Stim_AudPrimaryFreq * T4Audio) > 0
              else:
                  PrimarySinWaveAud = (1 + modulation_index * np.sin(2 * np.pi * CurrentStimParams.Stim_AudPrimaryFreq * T4Audio + Phas1)) * np.sin(2 * np.pi * CurrentStimParams.Stim_AudFc * T4Audio)  # Equation for SIngle Modulation

              if CurrentStimParams.Stim_AudSecondaryFreq > 0:
                  if CurrentStimParams.Stim_AudFreqStyle == 'Isochrone':
                      SecondarySinWaveAud = np.sin(2 * np.pi * CurrentStimParams.Stim_AudSecondaryFreq * T4Audio) > 0
                  else:
                      SecondarySinWaveAud = (1 + modulation_index * np.sin(2 * np.pi * CurrentStimParams.Stim_AudSecondaryFreq * T4Audio))
              else:
                  SecondarySinWaveAud = 1

              AudSignal = PrimarySinWaveAud * SecondarySinWaveAud
              if CurrentStimParams.Stim_AudFreqStyle == 'Isochrone':
                  AudSignal = AudSignal * np.sin(2 * np.pi * CurrentStimParams.Stim_AudFcFc * T4Audio) > 0

          elif CurrentStimParams.AudModulation == 'FM':
              # Paper : DOI: 10.1109/89.701371 for single and nested FM modulation
              # x(t) = A sin[2πfct + I sin(2πfmt)] Single Modulation
              # x(t) = A sin[2πfct + Im1 sin(2πfm1t + Im2 sin(2πfm2t))] NestedModulation
              FMModrange = 50  # FM modulation frequency range
              if CurrentStimParams.Stim_AudFreqStyle == 'Isochrone':
                  if CurrentStimParams.AudSecondaryFreq > 0:
                      AudSignal_PreFc = np.sin(2 * np.pi * CurrentStimParams.Stim_AudPrimaryFreq * T4Audio) > 0 * np.sin(2 * np.pi * CurrentStimParams.Stim_AudSecondaryFreq * T4Audio) > 0
                  else:
                      AudSignal_PreFc = np.sin(2 * np.pi * CurrentStimParams.Stim_AudPrimaryFreq * T4Audio) > 0
                  AudSignal = 2 * (AudSignal_PreFc * ((np.sin(2 * np.pi * CurrentStimParams.Stim_AudFc * T4Audio)) > 0) - 0.5)
              else:
                  if CurrentStimParams.Stim_AudSecondaryFreq > 0:
                      AudSignal = np.sin(2 * np.pi * CurrentStimParams.Stim_AudFc * T4Audio + FMModrange * np.sin(2 * np.pi * CurrentStimParams.Stim_AudPrimaryFreq * T4Audio + FMModrange * np.sin(2 * np.pi * CurrentStimParams.Stim_AudSecondaryFreq * T4Audio)))  # Nested
                  else:
                      AudSignal = np.sin(2 * np.pi * CurrentStimParams.Stim_AudFc * T4Audio + FMModrange * np.sin(2 * np.pi * CurrentStimParams.Stim_AudPrimaryFreq * T4Audio))  # SingleFreq
    AudSignal = AudSignal[:,np.newaxis] # add additional dimension
    AudSignal2=np.repeat(AudSignal,2,axis=1) # Psychopy takes nx2 as audio stim.

    AudSignal2=np.repeat(AudSignal,2,axis=1) # Psychopy takes nx2 as audio stim.

    
    #CreateComponents
    Movie01 = visual.MovieStim3(win=win, name='Movie01', units='norm',loop=True, noAudio = True, filename=VideoFile, ori=0.0, pos=(0, 0),size=(CurrentStimParams.Stim_MovieSize, CurrentStimParams.Stim_MovieSize), opacity=.1,  depth=0) #Define movie stim
    RectBox = visual.Rect(win=win, name='Rect01', width=(CurrentStimParams.Stim_RectSize,CurrentStimParams.Stim_RectSize)[0], height=(CurrentStimParams.Stim_RectSize, CurrentStimParams.Stim_RectSize)[1], ori=0.0, pos=(0, 0), lineWidth=0.0, colorSpace='rgb',  units='norm', lineColor=(1,-1,-1), fillColor='white', opacity=CurrentStimParams.Stim_RectangleOpacity, depth=0.0, interpolate=True) #Define Visual stim
    Aud01 = sound.Sound(AudSignal2, secs=CurrentStimParams.Stim_Duration, stereo=True, hamming=False,sampleRate =44100, name='Aud01',loops=10) #Specify Audio parameters
    Aud01.setVolume(CurrentStimParams.Stim_AudioVolume,log=True) #Adjust gain as specified in protocol

    Cross = visual.ShapeStim(win=win, name='Cross01', vertices='cross', size=[.01], ori=0.0, pos=(0, 0), lineWidth=1.0, colorSpace='rgb', lineColor=[1,0,0], fillColor=[1,0,0], opacity=None, interpolate=True)

    Distractors=[]
    Count_NumTargets=0
    for imageloc in TargetLocations:
        # RectBox =   visual.ImageStim(win=win, name='image'+str(Count_NumTargets), image='.\MediaResources\Distractor.png', mask=None, ori=0.0, pos=(imageloc[0]*.75,imageloc[1]*.75), size=(0.4, 0.4), color=[1,1,1], colorSpace='rgb', opacity=1, borderColor=(1,-1,-1), flipHoriz=False,units='norm', flipVert=False, texRes=128.0, interpolate=True,  depth=0.0)
        Distractors.append(visual.Rect(win=win, name='image'+str(Count_NumTargets), width=.3, height=.3, ori=0.0, pos=(imageloc[0]*.75,imageloc[1]*.75), lineWidth=10.0, colorSpace='rgb',  units='norm', lineColor=(-1,-1,-1), fillColor='white', opacity=1, depth=0.0, interpolate=True)) #Define Visual stim)
        Count_NumTargets+=1


    ImageList = np.stack(glob.glob('.\\Images\\*.bmp'))  # Get Stored Image list
    Images4Trial=np.random.choice(len(ImageList), PAL2Execute.PAL_TotalStims[0], replace=False)

# Get Correct Targets
    CorrectTargets=[]
    CorrectTargetLocs=np.random.choice(len(TargetLocations), PAL2Execute.PAL_TotalStims[0], replace=False)

    Count_NumTargets=0

    for stim in range(PAL2Execute.PAL_TotalStims[0]):
        CorrectTargets.append(visual.ImageStim(win=win, name='CorrectTar'+str(Count_NumTargets), image=ImageList[Images4Trial[stim]], mask=None, ori=0.0, pos=(TargetLocations[CorrectTargetLocs[stim]][0]*.75,TargetLocations[CorrectTargetLocs[stim]][1]*.75), size=(0.4, 0.4), color=[1,1,1], colorSpace='rgb', opacity=1, flipHoriz=False,units='norm', flipVert=False, texRes=128.0, interpolate=True, depth=0.0))
        Count_NumTargets+=1

# # Test Components
# Timekeep=core.Clock()
# t0=Timekeep.getTime()

# win.flip()
# # core.wait(1)
# Movie01.opacity=.5
# Movie01.setAutoDraw(True)
# RectBox.draw()
# # Movie01.setAutoDraw(False)
# # RectBox.color=(1,1,1)
# RectBox.draw()
# Cross.setAutoDraw(True)
# while Timekeep.getTime()-t0<5:
#     RectBox.opacity=1
#     RectBox.draw()
#     win.flip()

# for TrialNum in range(PAL2Execute.PAL_TotalStims[0]):

#     # Distractors


# CorrectTargetLocs=np.random.choice(len(TargetLocations), NumStims, replace=False)
#     Images4Trial=np.random.choice(len(ImageList), NumStims, replace=False)
#     DistractorRevealOrder=(linspace(0,len(Distractors)-1 ,len(Distractors)-1,dtype='int'))
#     shuffle(DistractorRevealOrder)

#     CorrectTargets=[]
#     for stim in range(NumStims):
#         CorrectTargets.append(visual.ImageStim(win=win, name='CorrectTar'+str(Count_NumTargets), image=ImageList[Images4Trial[stim]], mask=None, ori=0.0, pos=(TargetLocations[CorrectTargetLocs[stim]][0]*.75,TargetLocations[CorrectTargetLocs[stim]][1]*.75), size=(0.2, 0.2), color=[1,1,1], colorSpace='rgb', opacity=1, flipHoriz=False,units='norm', flipVert=False, texRes=128.0, interpolate=True, depth=0.0))
# win.close()
    return Movie01, RectBox, Aud01, Cross, Distractors, CorrectTargets, TargetLocations, CorrectTargetLocs, AudSignal2
    # return  RectBox, Cross, Distractors, CorrectTargets, TargetLocations, CorrectTargetLocs
