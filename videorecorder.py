#1 exiba se eu quiser pra eu calibrar -> ok 
#2 grave apenas o sensor -> ok
#3 formate o video com a data atual -> ok
#5 se audit==true, recorte videos salvos e coloque em outra pasta -> ok
#6 exiba dimensoes, fps, timestamp, nome do arquivo -> ok
#7 erros leves == log, erros criticos == email -> ok

### tempo minimo de gravacao em FPS ###
def flag_videowrite(set_videowriterfps, set_videoduration, amount_frames):
    minutes_in_seconds = set_videoduration * 60
    flag_amount_frames = set_videowriterfps * minutes_in_seconds
    min_qtdframes = flag_amount_frames

    if amount_frames <= min_qtdframes:
        log = f"[Time Video Writer ERROR]-{dirvideosave}, videowriter time is less than desired - amount_frames:{amount_frames}, min_qtdframes{min_qtdframes}"
        register_log(csv_path=log_path, log=log, logtime=timepath) 

### send alerts to email ###
'''
def send_emails():
    import smtplib
    import email.message

    corpo_email = """
    <p>Parágrafo1</p>
    <p>Parágrafo2</p>
    """

    msg = email.message.Message()
    msg['Subject'] = "Assunto"
    msg['From'] = 'remetente'
    msg['To'] = 'destinatario'
    password = 'senha' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

    pass 
'''

### time ###
def timenow():
    from datetime import datetime
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_time

### display ###
def display_sensor(sensorframe, original_dimensions, sensor_dimensions, fps, timestamp):
    original_dimensions = f"Original: {original_dimensions}"
    sensor_dimensions = f"Sensor: {sensor_dimensions}"
    fps = f"FPS: {fps}"
    timestamp = f"{timestamp}"
    
    cv2.putText(sensorframe, original_dimensions, (20, 20),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 0, 0), 3)
    
    cv2.putText(sensorframe, sensor_dimensions, (20, 40),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 0, 0), 3)

    cv2.putText(sensorframe, fps, (20, 60),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 0, 0), 3)
    
    cv2.putText(sensorframe, timestamp, (20, 80),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 0, 0), 3)
    #--contrast
    cv2.putText(sensorframe, original_dimensions, (20, 20),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1)
    
    cv2.putText(sensorframe, sensor_dimensions, (20, 40),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1)

    cv2.putText(sensorframe, fps, (20, 60),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1)
    
    cv2.putText(sensorframe, timestamp, (20, 80),
                cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 255, 255), 1)

### automatic audit videos ###
def automatic_audit():

    pass


### log ###

def register_log(csv_path, log, logtime):
    import csv
    with open(csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([log, logtime])


### read config file ###
from configparser import ConfigParser

parser = ConfigParser()
parser.read("config.cfg")

audit = parser.getboolean("interface", "audit")
private_mode = parser.getboolean("interface", "private_mode")
audit_duration_minutes = parser.getint("interface", "audit_duration_minutes")


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

log_path = dir_path + "/log.csv"


### capturing ###
import cv2
import numpy as np

if len(cam) == 1:
    cam = int(cam)
else:
    cam = str(cam)

cap = cv2.VideoCapture(cam)

timepath = timenow()
dirvideosave = dir_videosave + f"/{timepath}" + ".mp4"

if (cap.isOpened()== False):
    log = f"[Video Capture ERROR] - {dirvideosave}"
    register_log(csv_path=log_path, log=log, logtime=timepath) 
 

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))



sensor_height = size_sensor_height - y
sensor_width = size_sensor_width - x

out = cv2.VideoWriter(dirvideosave, cv2.VideoWriter_fourcc('M','J','P','G'), videowriterfps, (sensor_width, sensor_height))

original_width = cap.get(3)
original_height= cap.get(4)
originalfps = int(cap.get(cv2.CAP_PROP_FPS))

qtdframes = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        videocrop = frame[y : size_sensor_height, x : size_sensor_width]

        now = timenow()
        display_sensor(sensorframe=videocrop, original_dimensions=(original_width, original_height), sensor_dimensions=(sensor_width, sensor_height), fps=(originalfps, videowriterfps), timestamp=now)

        qtdframes += 1
        out.write(videocrop)
       
        if not private_mode:
            cv2.imshow('original', frame) 
            cv2.imshow('sensor', videocrop) 
            
        if cv2.waitKey(delayfps) == 27:
            break
    else: 
        break

flag_videowrite(set_videowriterfps=videowriterfps, set_videoduration=videoduration_minutes, amount_frames=qtdframes)
cap.release()
out.release()
cv2.destroyAllWindows()

