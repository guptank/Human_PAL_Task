import nidaqmx
from nidaqmx.constants import (LineGrouping)
import time, os, csv
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors

system = nidaqmx.system.System.local()
nDevices=[]
for device in system.devices:
    nDevices.append(device.name=='USB-6001')
    print(device.name)

Device_NI6001_Exists=any(nDevices)
with nidaqmx.Task() as task:
    task.do_channels.add_do_chan("Dev1/port0/line0:7",line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
    task.write(210)
    core.wait(0.002)
    task.write(0)