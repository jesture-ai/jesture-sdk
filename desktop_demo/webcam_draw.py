from threading import Thread
import logging
import cv2

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from skimage import io
import numpy as np

from thread_camera import ThreadCamera
from utils import load_image_with_alpha, overlay_alpha
from utils import draw_text, draw_multiline_text, draw_skeleton


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')


class WebcamDrawStream:
    def __init__(self, jesture_runner, cam_id=0, width=640, height=480, 
                 hand_box_tl=None, hand_box_br=None, draw_hand_box=False):
        '''
        Args:
            hand_box_tl (tuple[2]): top-left corner of ui box with hands
            hand_box_br (tuple[2]): bottom-right corner of ui box with hands
        '''
        
        self.jesture_runner = jesture_runner
        self.stream = cv2.VideoCapture(cam_id)
        self.width = width
        self.height = height
        self.hand_box_tl = hand_box_tl
        self.hand_box_br = hand_box_br
        
        self.draw_hand_box = draw_hand_box
            
        # capture settings
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    
    def start(self):
        logging.debug('[WebcamDrawStream] Starting a thread...')
        self.thread = Thread(name='Camera-Draw Python Thread', target=self.update, args=())
        self.thread.start()
        logging.debug('[WebcamDrawStream] Thread started.')
        return self
    
    def update(self):
        i = 0
        while not self.stopped:
            (self.grabbed, frame) = self.stream.read()
            
            if i == 0:
                print(frame.shape)
                i = 1
            
#             frame = cv2.resize(frame, (self.width, self.height))
            
            # get current hand keypoints
            left_keypoints = self.jesture_runner.get_hand_keypoints(
                'left_keypoints', mirror=False)
            right_keypoints = self.jesture_runner.get_hand_keypoints(
                'right_keypoints', mirror=False)
            
            # draw skeletons using hand keypoints
            frame = draw_skeleton(frame, left_keypoints)
            frame = draw_skeleton(frame, right_keypoints)
            
            # TODO: move all `ImageDraw` tasks to a separate thread or do it asynchronously
            # draw a special box for scaled keypoints
            if self.draw_hand_box:
                frame = Image.fromarray(frame if type(np.array([])) == type(frame) else frame.get())
                draw = ImageDraw.Draw(frame, "RGBA")
                draw.rectangle((self.hand_box_tl, self.hand_box_br), fill=(0, 0, 0, 127), outline=(235, 190, 63, 255))
                frame = np.array(frame).astype(np.uint8)
                
            # scaled hand keypoints stuff
            scale_x = (self.hand_box_br[0] - self.hand_box_tl[0]) // 2
            scale_y = self.hand_box_br[1] - self.hand_box_tl[1]
            scale = (scale_x, scale_y)
            # mind that it is not yet mirrored
            shift_left = (self.hand_box_tl[0], self.hand_box_tl[1])  
            # (self.hand_box_tl[0], self.hand_box_tl[1])
            shift_right = (self.hand_box_tl[0]+scale_x, self.hand_box_tl[1])  
            # (self.width-self.hand_box_tl[0]+scale_x, self.hand_box_tl[1])
        
            # draw scaled keypoints
            scaled_left_keypoints = self.jesture_runner.get_hand_keypoints(
                'scaled_left_keypoints', mirror=False, scale=scale, shift=shift_right)  # right, because not yet mirrored
            scaled_right_keypoints = self.jesture_runner.get_hand_keypoints(
                'scaled_right_keypoints', mirror=False, scale=scale, shift=shift_left)  # left, because not yet mirrored
            frame = draw_skeleton(frame, scaled_left_keypoints, indices=False)
            frame = draw_skeleton(frame, scaled_right_keypoints, indices=False)
            
            # save to the field
            self.frame = frame
            
        logging.debug('[WebcamDrawStream] Frame loop finished.')
        self.stream.release()
        logging.debug('[WebcamDrawStream] Capture released.')
    
    def read(self):
        return self.frame
    
    def stop(self) :
        logging.debug('[WebcamDrawStream] Stopping...')
        self.stopped = True
        self.thread.join()
        logging.debug('[WebcamDrawStream] Camera thread joined.')
        

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()
