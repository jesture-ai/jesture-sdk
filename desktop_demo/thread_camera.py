import cv2
from threading import Thread


class WebcamVideoStream:
    def __init__(self, src=0, width=320, height=240):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    
    def start(self):
        self.thread = Thread(name='thread_camera_python', target=self.update, args=())
        self.thread.start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
        self.thread.join()
    
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True
