clear all 
clc
close all
Frame=uint8(zeros(1080,1920,3));% For alienware monitor resoultion
TotalTime=60;

v = VideoWriter('BlankVideo.mp4','MPEG-4');
v.FrameRate=30;
v.Quality = 50;
open(v)
for iter_frame=1:v.FrameRate*TotalTime
    writeVideo(v,Frame);
end
close(v)