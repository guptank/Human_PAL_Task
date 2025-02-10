Timeout=100;
WaitDur=0.5;
DurDisp=5;


%% Create and Configure the DataAcquisition Object
dq = daq("ni"); %Create daq Object
addinput(dq, "NI6363", "ai0", "Voltage"); %for measuring the audio feed
addinput(dq, "NI6363", "ai1", "Voltage"); % for measuring the video feed
dq.Rate = 44100; %Sample AV channels at 44.1KHz (which is the audio frequency)

%% Plot Live Data as It Is Acquired
% During a background acquisition, the DataAcquisition can handle acquired data in a specified way using the |ScansAvailableFcn| property.
dq.ScansAvailableFcn = @(src,evt) plotDataAvailable(src, evt);

%% Set ScansAvailableFcnCount
% By default, the ScansAvailableFcn is called 10 times per second. Modify
% the |ScansAvailableFcnCount| property to decrease the call frequency.
% The ScansAvailableFcn will be called when the number of points
% accumulated exceeds this value. Set the ScansAvailableFcnCount to the
% rate, which results in one call to ScansAvailableFcn per second.
dq.ScansAvailableFcnCount = round(dq.Rate*DurDisp);

%% Start the Background Acquisition
% Use |start| to start the background acquisition.  

start(dq, "Duration", seconds(Timeout))


%%
% There are no other calculations to perform and the acquisition is set to
% run for the entire five seconds. Use |pause| in a loop to monitor the
% number of scans acquired for the duration of the acquisition.

while dq.Running
    pause(WaitDur)
   % fprintf("While loop: Scans acquired = %d\n", dq.NumScansAcquired)
end

fprintf("Acquisition stopped with %d scans acquired\n", dq.NumScansAcquired);

%% Capture a Unique Event in Incoming Data
% Acquire continuously until a specific condition is met. In this example,
% acquire until the signal equals or exceeds 1 V.

%%
dq.ScansAvailableFcn = @(src,evt) stopWhenEqualsOrExceedsOneV(src, evt);

%%
% Configure the DataAcquisition to acquire continuously. The listener detects the
% 1V event and calls |stop|.
start(dq, "continuous");

%%
% Use |pause| in a loop to monitor the number of scans acquired for the
% duration of the acquisition. Note that the status string displayed by the
% |ScansAvailableFcn| may appear before the last status string displayed by
% the while loop.
while dq.Running
    pause(WaitDur)
%     fprintf("While loop: Scans acquired = %d\n", dq.NumScansAcquired)
end

fprintf("Acquisition has terminated with %d scans acquired\n", dq.NumScansAcquired);

dq.ScansAvailableFcn = [];

%%

function plotDataAvailable(src, ~)
    [data, timestamps, ~] = read(src, src.ScansAvailableFcnCount, "OutputFormat", "Matrix");
    plot(timestamps, data); 
end

function stopWhenEqualsOrExceedsOneV(src, ~)
    [data, timestamps, ~] = read(src, src.ScansAvailableFcnCount, "OutputFormat", "Matrix");
    if any(data >= 1.0)
        disp('Detected voltage exceeds 1V: stopping acquisition')
        % stop continuous acquisitions explicitly 
        src.stop()
        plot(timestamps, data)
    else
%         disp('Continuing to acquire data')
    end
end
