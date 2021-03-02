from threading import Thread
import logging
import cv2


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')


class ThreadCamera:
    def __init__(self, cam_id=0, width=640, height=480):
        self.stream = cv2.VideoCapture(cam_id)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    
    def start(self):
        self.thread = Thread(name='Camera Python Thread', target=self.update, args=())
        self.thread.start()
        return self
    
    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
        logging.debug('[ThreadCamera] Frame loop finished.')
        self.stream.release()
        logging.debug('[ThreadCamera] Capture released.')
    
    def read(self):
        return self.frame
    
    def stop(self) :
        logging.debug('[ThreadCamera] Stopping...')
        self.stopped = True
        self.thread.join()
        logging.debug('[ThreadCamera] Camera thread joined.')

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()
