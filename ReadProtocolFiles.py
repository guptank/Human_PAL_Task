# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 12:32:08 2022

@author: agupta001
"""

def GetAllDataFiles():
    import os
    import pandas as pd

    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    TargetLocations=[[-1, -1], [-0.33, -1], [0.33,-1], [1,-1], [1,-0.33],[1,0.33],[1,1],[0.33, 1],[-0.33,1],[-1,1],[-1,0.33], [-1,-0.33]]

    #define Files Location
    ProtocolFilelocation='.\\Protocols\\Protocol.xls'
    PALFileLocation='.\\Protocols\\PALTask.xlsx'

    Protocol= pd.read_excel(ProtocolFilelocation, sheet_name="Protocol1")

    # Get Current Task to execute
    CurrSeqFile = open("seq.txt", "r+")
    CurrentTask = int(CurrSeqFile.readline())
    CurrSeqFile.close()

    # read the PAL task to execute for the current Stim
    CurrentStimParams=Protocol.iloc[CurrentTask]
    PAL2Execute= pd.read_excel(PALFileLocation, sheet_name=CurrentStimParams.PAL_task)
    return CurrentStimParams, PAL2Execute, TargetLocations
