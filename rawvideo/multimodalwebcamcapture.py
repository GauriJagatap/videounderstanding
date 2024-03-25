'''
Fetch audio and video concurrently from webcam feed.
Pass past 2-sec buffer to a sample function that processes both audio and video, return the value to print to webcam feed.
'''
import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os
import concurrent.futures
import numpy as np
import math

def capture_audio(stream, audio_frames, fpb=1024, vbs=60):
    while len(audio_frames) <= vbs:
        data = np.frombuffer(stream.read(fpb),dtype=np.int16)
        audio_frames.append(data)
        if len(audio_frames) > vbs:
            audio_frames = audio_frames[1:]
            break
    return audio_frames

def capture_video(video_cap, video_frames, vbs):
    while len(video_frames) <= vbs:
        ret, video_frame = video_cap.read()
        if not ret:
            break
        video_frames.append(video_frame)
        if len(video_frames) > vbs:
            video_frames = video_frames[1:]
            break
    return video_frames

# placeholder multimodal function
def av_metrics(aud_buffer,vid_buffer):
    val = 0
    lum = 0
    for aud in aud_buffer:
        val += 20 * math.log10(np.linalg.norm(aud))

    for image in vid_buffer:    
        luminance = 0.114 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.299 * image[:, :, 2]
        lum += np.linalg.norm(luminance)/(image.shape[0]*image.shape[1])

    return val/len(aud_buffer), lum/len(vid_buffer)
  
# initialize video streaming
vidcap = cv2.VideoCapture(0)
vid_buffer = []
fps = 30
buff_time = 2
vidbufsize = fps * buff_time # save last 2 sec of video frames in vid_buffer = 2 x 30fps
# initialize audio streaming
rate = 44100
frames_per_buffer = rate // fps
channels = 1
format = pyaudio.paInt16
audio = pyaudio.PyAudio()
stream = audio.open(format=format, channels=channels,
                                    rate=rate,
                                    input=True,
                                    frames_per_buffer=frames_per_buffer)
stream.start_stream()
aud_buffer = []

# Use ThreadPoolExecutor to run both functions in separate threads
val, luminance = 0,0
while True:
    tt = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit both tasks and get their futures
        audio_future = executor.submit(capture_audio, stream, aud_buffer, frames_per_buffer, vidbufsize)
        video_future = executor.submit(capture_video, vidcap, vid_buffer, vidbufsize)

        # Wait for both tasks to complete and collect their results
        aud_buffer = audio_future.result()
        vid_buffer = video_future.result()
      
    image = vid_buffer[-1]
    val, luminance = av_metrics(aud_buffer,vid_buffer)
    cv2.putText(image, '2-sec av sound level:' + str(round(val,2))+'dB', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
    cv2.putText(image, '2-sec av luminance:'+str(round(float(luminance),2)), (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
    cv2.imshow('video frame', image)
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break     
    print(time.time()-tt)   

vidcap.release()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
