import cv2 
import datetime 

data = cv2.VideoCapture("videos/teste.mp4") 

frames = data.get(cv2.CAP_PROP_FRAME_COUNT) 

fps = int(data.get(cv2.CAP_PROP_FPS)) 

seconds = int(frames / fps) 

video_time = str(datetime.timedelta(seconds=seconds)) 

print("duration in seconds:", seconds) 
print("video time:", video_time) 