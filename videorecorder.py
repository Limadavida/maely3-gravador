#1 exiba se eu quiser pra eu calibrar 
#2 grave apenas o sensor -> ok
#3 formate o video com a data atual -> ok
#5 se audit==true, recorte videos salvos e coloque em outra pasta -> ok
#6 exiba dimensoes, fps, timestamp, nome do arquivo
#7 erros leves == log, erros criticos == email

### tempo minimo de gravacao em FPS ###
def flag_videowrite(set_videowriterfps, set_videoduration, amount_frames):
    minutes_in_seconds = set_videoduration * 60
    flag_amount_frames = set_videowriterfps * minutes_in_seconds
    min_qtdframes = flag_amount_frames

    if amount_frames <= min_qtdframes:
        print("error critico tempo gravado menor q 5minutes", flag_amount_frames)



#flag_videowrite(set_videowriterfps=60, set_videoduration=5, amount_frames=990)

### time ###
def timenow():
    from datetime import datetime
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_time

### display ###
def display_sensor():
    pass

### log ###
import csv

def register_log(csv_path, log, logtime):
    with open(csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([log, logtime])


### read config file ###
from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.cfg")

audit = parser.getboolean("interface", "audit")
private_mode = parser.getboolean("interface", "private_mode")

cam = parser.get("config", "cam")
path_videorecorder = parser.get("config", "path_video_recorder")
delayfps = parser.getint("config", "delayfps")
videowriterfps = parser.getint("config", "video_writer_fps")
videoduration_minutes = parser.getint("config", "video_duration_minutes")

x = parser.getint("sensor", "x")
size_sensor_width = parser.getint("sensor", "size_sensor_width")
y = parser.getint("sensor", "y")
size_sensor_height = parser.getint("sensor", "size_sensor_height")



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
    #flag video out
  print("Error critico opening video stream or file")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, sensor_size)
timepath = timenow()
dirvideosave = dir_videosave + f"/{timepath}" + ".mp4"

sensor_height = size_sensor_height - y
sensor_width = size_sensor_width - x

out = cv2.VideoWriter(dirvideosave, cv2.VideoWriter_fourcc('M','J','P','G'), videowriterfps, (sensor_width, sensor_height))


print(videowriterfps)
#cap.set(3,300)
#cap.set(4,300)
#cap.set(15, 0.1)

print("width={}".format(cap.get(3)))
print("height={}".format(cap.get(4)))
#print("exposure={}".format(cap.get(15)))


fps = cap.get(cv2.CAP_PROP_FPS)
#print(fps)

qtdframes = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        videocrop = frame[y : size_sensor_height, x : size_sensor_width]
        
        qtdframes += 1
        out.write(videocrop)

        #if not private:
            #print("running in private_mode")
        if not private_mode:
            cv2.imshow('original', frame) 
            cv2.imshow('sensor', videocrop) 
            
        if cv2.waitKey(delayfps) == 27:
            break


    else: 
        print(f"Break the loop if ret is false, ret={ret}")
        break

print(f"motante de frames {qtdframes}")
flag_videowrite(set_videowriterfps=videowriterfps, set_videoduration=videoduration_minutes, amount_frames=qtdframes)
cap.release()
out.release()
cv2.destroyAllWindows()

