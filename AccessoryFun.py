# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:25:47 2022

@author: agupta001
""" 
import nidaqmx
from nidaqmx.constants import (LineGrouping)
import os, csv
import pandas as pd

def SaveLogFiles(TrialData, FrameLogs, AudSignal, FrameN, DataFolderPath):
    
    with open(DataFolderPath+os.sep+'FramesInfo.csv', 'w',newline='') as f:
        writer = csv.writer(f)      
        writer.writerow(['FrameNum', 'Frametime', 'RectOpacity', 'RectCol_R','RectCol_G','RectCol_B']) # write the header
        for iter in range(FrameN):# write the data
            writer.writerow(FrameLogs[iter])
    
    with open(DataFolderPath+os.sep+'AudioInfo.csv', 'w',newline='') as f:
        writer = csv.writer(f)      
        #writer.writerow(['FrameNum', 'Frametime', 'RectOpacity', 'RectCol_R','RectCol_G','RectCol_B']) # write the header
        for iter in AudSignal:# write the data
            writer.writerow(iter)
    
    TrialData.to_csv(DataFolderPath+os.sep+'TrialsInfo.csv', header = True, index=True)
    
def SendSignals(Device_NI6001_Exists,EventNum,core):
    if Device_NI6001_Exists:
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan("NI6001/port0/line0:7",line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
            task.write(EventNum)
            core.wait(0.002)
            task.write(False)
    