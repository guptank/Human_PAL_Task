clear all
clc
close all

showerror_Device=false;
DevList=daqlist;

if ~isempty(DevList)
    Dev2Use=find(matches([DevList.DeviceID], 'NI6363'));
    
    if isempty(Dev2Use)
        showerror_Device=true;
    end
else 
    showerror_Device=true;
end
% showerror_Device=true;

if showerror_Device
    error('NI6363 NOT Found! Please ensure that the device is connected. If NI6363 is already connected ensure that it is showing up in NIMAX > Devices and Interfaces section with name "NI6363"');
else
    Dev=daq('ni'); 
    Dev.Rate=44100;
    addinput(Dev, "NI6363", "ai0", "Voltage");
     addinput(Dev, "NI6363", "ai1", "Voltage");
     Dev.ScansAvailableFcn = @(src,evt) plot(src, evt);
     Dev.ScansAvailableFcnCount = 44100;
     start(Dev, "Duration", seconds(5))
%     data= read(Dev, seconds(2), "OutputFormat", "Matrix");
%     plot(data)
    
end


