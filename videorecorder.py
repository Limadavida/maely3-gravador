#1 exiba se eu quiser pra eu calibrar ok
#2 grave apenas o sensor
#3 formate o video com a data atual
#5 se audit==true, recorte videos salvos e coloque em outra pasta

### video recorder function ###
def write_video(file_path, frames, fps):
    """
    Writes frames to an mp4 video file
    :param file_path: Path to output video, must end with .mp4
    :param frames: List of PIL.Image objects
    :param fps: Desired frame rate
    """

    #w, h = frames[0].size
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    #writer = cv.VideoWriter(file_path, fourcc, fps, (w, h))
    writer = cv2.VideoWriter(file_path, fourcc, fps, (600, 600))

    for frame in frames:
        writer.write(pil_to_cv(frame))

    writer.release() 

def initializeVideoWriter(dirvideosave, video_width, video_height, videoStream, fps):
    #outputVideoPath = "audit/auditoria.avi"
    #outputVideoPath = f"audit/auditoria{number_random}.avi"
    #outputVideoPath = dirvideosave + ".mp4"
    outputVideoPath = "videos/1" + ".avi"

    #sourceVideofps = videoStream.get(cv2.CAP_PROP_FPS)
    sourceVideofps = fps
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    return cv2.VideoWriter(outputVideoPath, fourcc, sourceVideofps,
                           (video_width, video_height), True)

def timenow():
    from datetime import datetime
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_time


### read config file ###
from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.cfg")

cam = parser.get("config", "cam")
private = parser.getboolean("config", "private")
path_videorecorder = parser.get("config", "path_videorecorder")
delayfps = parser.getint("config", "delayfps")
videowriterfps = parser.getint("config", "videowriterfps")


sensory = parser.getint("sensor", "y")
sensorh = parser.getint("sensor", "h")
sensorx = parser.getint("sensor", "x")
sensorw = parser.getint("sensor", "w")

### relative path ###
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

dir_videosave = dir_path + "/videos"
if not os.path.isdir(dir_videosave):
    os.mkdir(dir_videosave)
    print("Criando Pasta {dir_videosave}")


dir_audit = dir_path + "/audit"
if not os.path.isdir(dir_audit):
    os.mkdir(dir_audit)
    print("Criando Pasta {dir_audit}")


### capturing ###
import cv2
import numpy as np

if len(cam) == 1:
    cam = int(cam)
else:
    cam = str(cam)

cap = cv2.VideoCapture(cam)
     
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        width = sensory+sensorh
        height = sensorx+sensorw
        videocrop = frame[sensory:width, sensorx:height]

        if not private:
            print("running in private_mode")
            cv2.imshow('original', frame) 
            cv2.imshow('sensor', videocrop) 
          
        if cv2.waitKey(delayfps) == 27:
            break

        now = timenow()
        dirvideosave = dir_videosave + f"/{now}"
        print(dirvideosave)
        #write_video(dirvideosave, dirvideosave, videocrop, videowriterfps)
        print(width)
        initializeVideoWriter(dirvideosave=dirvideosave, video_width=width, video_height=height, videoStream=videocrop, fps=videowriterfps)
    
    else: 
        print(f"Break the loop if ret is false, ret={ret}")
        break

cap.release()
cv2.destroyAllWindows()


'''
def initializeVideoWriter(video_width, video_height, videoStream):
    #outputVideoPath = "audit/auditoria.avi"
    outputVideoPath = f"audit/auditoria{number_random}.avi"
    sourceVideofps = videoStream.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    return cv2.VideoWriter(outputVideoPath, fourcc, sourceVideofps,
                           (video_width, video_height), True)

-----

def write_video(file_path, frames, fps):
    """
    Writes frames to an mp4 video file
    :param file_path: Path to output video, must end with .mp4
    :param frames: List of PIL.Image objects
    :param fps: Desired frame rate
    """

    w, h = frames[0].size
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv.VideoWriter(file_path, fourcc, fps, (w, h))

    for frame in frames:
        writer.write(pil_to_cv(frame))

    writer.release() 

'''