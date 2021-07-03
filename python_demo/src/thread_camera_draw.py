from threading import Thread
import logging
import cv2

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from skimage import io
import numpy as np

from .utils import draw_skeleton


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')


class ThreadCameraDraw:
    def __init__(self, jesture_runner, cam_id=0, width=640, height=480, 
                 hand_box_tl=None, hand_box_br=None, draw_hand_box=False, mirror=False):
        '''
        Args:
            hand_box_tl (tuple[2]): top-left corner of ui box with hands
            hand_box_br (tuple[2]): bottom-right corner of ui box with hands
        '''
        
        self.jesture_runner = jesture_runner
        self.cam_id = cam_id
        self.width = width
        self.height = height
        
        self.stream = cv2.VideoCapture(self.cam_id)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        
        self.hand_box_tl = hand_box_tl
        self.hand_box_br = hand_box_br
        self.draw_hand_box = draw_hand_box
        
        self.mirror = mirror
        
    def _scale_and_shift(self, keypoints, scale, shift):
        keypoints = np.array([scale[0], scale[1], 1]) * keypoints + np.array([shift[0], shift[1], 0])
        return keypoints
    
    def start(self):
        logging.debug('[ThreadCameraDraw] Starting a thread...')
        self.thread = Thread(name='Camera-Draw Python Thread', target=self.update, args=())
        self.thread.start()
        logging.debug('[ThreadCameraDraw] Thread started.')
        return self
    
    def update(self):
        logged = False
        while not self.stopped:
            (self.grabbed, frame) = self.stream.read()
            
            if not self.grabbed:
                continue
            
            display_height, display_width = frame.shape[:2]
            if not logged:
                print('Camera params was set to:', self.width, self.height)
                print('Real params are:', display_width, display_height)
            
            frame = cv2.resize(frame, (self.width, self.height))
            
            # get current hand keypoints
            left_keypoints = self.jesture_runner.get_hand_keypoints('left_keypoints')
            right_keypoints = self.jesture_runner.get_hand_keypoints('right_keypoints')
            
            left_keypoints = np.clip(left_keypoints, 0.0, 1.0)  # !!!
            right_keypoints = np.clip(right_keypoints, 0.0, 1.0)  # !!!
            
            # scale absolute keypoints by the actual display image size
            left_keypoints = left_keypoints * np.array([display_width, display_height, 1.0])
            if not logged: print(left_keypoints)
            right_keypoints = right_keypoints * np.array([display_width, display_height, 1.0])
            if not logged: print(right_keypoints)
            if self.mirror:
                left_keypoints[:,0] = display_width - left_keypoints[:,0]
                right_keypoints[:,0] = display_width - right_keypoints[:,0]
            
            # draw skeletons using screen-sized hand keypoints
#             frame = draw_skeleton(frame, left_keypoints)
            frame = draw_skeleton(frame, right_keypoints)
            
            # TODO: move all `ImageDraw` tasks to a separate thread or do it asynchronously
            # draw a special box for scaled keypoints
            if self.draw_hand_box:
                frame = Image.fromarray(frame if type(np.array([])) == type(frame) else frame.get())
                draw = ImageDraw.Draw(frame, "RGBA")
                draw.rectangle((self.hand_box_tl, self.hand_box_br), fill=(0, 0, 0, 127), outline=(235, 190, 63, 255))
                frame = np.array(frame).astype(np.uint8)
                
            # get the scaled hand keypoints
            scaled_left_keypoints = self.jesture_runner.get_hand_keypoints('scaled_left_keypoints')
            scaled_right_keypoints = self.jesture_runner.get_hand_keypoints('scaled_right_keypoints')
            
            scaled_left_keypoints = np.clip(scaled_left_keypoints, 0.0, 1.0)  # !!!
            scaled_right_keypoints = np.clip(scaled_right_keypoints, 0.0, 1.0)  # !!!
            
            # scale and shift them to be in a proper place on the display image
            scale_x = (self.hand_box_br[0] - self.hand_box_tl[0]) // 2
            scale_y = self.hand_box_br[1] - self.hand_box_tl[1]
            scale = (scale_x, scale_y)
            shift_left = (self.hand_box_tl[0], self.hand_box_tl[1])  
            shift_right = (self.hand_box_tl[0] + scale_x, self.hand_box_tl[1])  
            scaled_left_keypoints = self._scale_and_shift(
                scaled_left_keypoints, scale=scale, shift=shift_left if self.mirror else shift_right)
            scaled_right_keypoints = self._scale_and_shift(
                scaled_right_keypoints, scale=scale, shift=shift_right if self.mirror else shift_left)
            
            # draw scaled keypoints
#             frame = draw_skeleton(frame, scaled_left_keypoints, indices=False)
            frame = draw_skeleton(frame, scaled_right_keypoints, indices=False)
            
            # save to the field
            self.frame = frame
            
            if not logged:
                logged = True
            
        logging.debug('[ThreadCameraDraw] Frame loop finished.')
        self.stream.release()
        logging.debug('[ThreadCameraDraw] Capture released.')
    
    def read(self):
        return self.frame
    
    def stop(self) :
        logging.debug('[ThreadCameraDraw] Stopping...')
        self.stopped = True
        self.thread.join()
        logging.debug('[ThreadCameraDraw] Camera thread joined.')
        

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()
