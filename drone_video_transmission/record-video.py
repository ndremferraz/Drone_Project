import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()
tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def video_stream():
    global keepRecording
    
    while keepRecording:
        
        frame = frame_read.frame
        
        if frame is not None and frame.size > 0:
            
            cv2.imshow("Tello Live Stream", frame)
            
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            keepRecording = False
            
        time.sleep(0.01)
    cv2.destroyAllWindows()

recorder = Thread(target=video_stream)
recorder.start()

try:
    time.sleep(10)  
finally:
    keepRecording = False
    recorder.join()
    tello.streamoff()
