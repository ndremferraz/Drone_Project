import time, cv2
from ultralytics import YOLO
from threading import Thread
from djitellopy import Tello

tello = Tello()
tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

model = YOLO('yolo11n_jul2_2025.pt')

def video_stream():
    global keepRecording
    
    while keepRecording:
        
        frame = frame_read.frame
        
        if frame is not None and frame.size > 0:
            
            cv2.imshow("Tello Live Stream", model(frame)[0].plot())
            
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            keepRecording = False
            
        time.sleep(1)
    cv2.destroyAllWindows()

recorder = Thread(target=video_stream)
recorder.start()

try:
    time.sleep(45)  
finally:
    keepRecording = False
    recorder.join()
    tello.streamoff()
