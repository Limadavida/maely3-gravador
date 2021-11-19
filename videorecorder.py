#1 exiba se eu quiser pra eu calibrar ok
#2 grave apenas o sensor
#3 formate o video com a data atual
#5 se audit==true, recorte videos salvos e coloque em outra pasta

### video recorder function ###


### time ###
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

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)

sensor_width = sensory+sensorh
sensor_height = sensorx+sensorw
sensor_size = (sensor_width, sensor_height)

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, sensor_size)

cap.set(3,300)
cap.set(4,300)
cap.set(15, 0.1)

print("width={}".format(cap.get(3)))
print("height={}".format(cap.get(4)))
print("exposure={}".format(cap.get(15)))


fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        #sensor_width = sensory+sensorh
        #sensor_height = sensorx+sensorw
        videocrop = frame[sensory:sensor_width, sensorx:sensor_height]

        out.write(videocrop)


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
        #initializeVideoWriter(dirvideosave=dirvideosave, video_width=width, video_height=height, videoStream=frame, fps=fps)
        outputVideoPath = "videos/1" + ".mp4"

        #sourceVideofps = videoStream.get(cv2.CAP_PROP_FPS)
        sourceVideofps = fps
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")

        #cv2.VideoWriter("videos/2" + ".mp4", fourcc, fps, frame_size, True)
    

    else: 
        print(f"Break the loop if ret is false, ret={ret}")
        break

cap.release()
out.release()
cv2.destroyAllWindows()


'''
def initializeVideoWriter(video_width, video_height, videoStream):
    #outputVideoPath = "audit/auditoria.avi"
    outputVideoPath = f"audit/auditoria{number_random}.avi"
    sourceVideofps = videoStream.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    return cv2.VideoWriter(outputVideoPath, fourcc, sourceVideofps,
                           (video_width, video_height), True)


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