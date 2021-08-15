from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import argparse
import cv2
import sys
import os

sys.path.append(os.path.abspath(".."))

from src.runner import JestureSdkRunner
from src.utils import load_image_with_alpha, overlay_alpha
from src.utils import draw_text, draw_multiline_text
from src.thread_camera import ThreadCamera

print('cv2.__version__:', cv2.__version__)  # 4.1.2 recommended


# pasrse args
parser = argparse.ArgumentParser(description='Collect hand keypoints data for gesture recognition fitting.')
parser.add_argument('--cam_id', type=int, default=0)
args = parser.parse_args()


# create the application window
name = 'Jesture SDK: Python Demo'
width, height = (640, 480)
cv2.namedWindow(name)
# cv2.resizeWindow(name, (width, height))
cv2.startWindowThread()

# load the logo image
logo_path = f'images/jesture_logo.png'
logo_img, logo_alpha = load_image_with_alpha(logo_path, remove_borders=True)

# set the ui elements positions
top_box_tl = (230, 10)
top_box_br = (630, 70)

left_box_tl = (70, 360)
left_box_br = (230, 420)

right_box_tl = (420, 360)
right_box_br = (580, 420)

# set the text positions
logo_loc = (10, 10)
left_text_loc = (80, 375)
right_text_loc = (430, 375)
dynamic_text_loc = (240, 25)
font = ImageFont.truetype("fonts/Comfortaa-Light.ttf", 24)

# start Jesture SDK Python runner
jesture_runner = JestureSdkRunner(
    cam_id=args.cam_id, 
    use_tracking=True, 
    use_static_gestures=True, 
    use_dynamic_gestures=True)
jesture_runner.start_recognition()

# start reading frames to display in the application window
cap = ThreadCamera(cam_id=args.cam_id, width=width, height=height)
cap.start()


selfie_mode = True
i = 0
while(True):
    if cap.frame is None:
        continue
    
    # get current webcam image
    frame = cap.frame[:,::-1,:] if selfie_mode else cap.frame  # TODO: read frames from dylib
    
    # get current hand gestures
    dynamic_gesture = jesture_runner.get_gesture('dynamic')
    left_gesture = jesture_runner.get_gesture('left_static')
    right_gesture = jesture_runner.get_gesture('right_static')
    
    # draw logo
    frame = overlay_alpha(logo_img[:,:,::-1], logo_alpha, frame, loc=logo_loc, alpha=1.0)
    
    # draw ui elements
    frame = Image.fromarray(frame)
    draw = ImageDraw.Draw(frame, "RGBA")
    draw.rectangle((top_box_tl, top_box_br), fill=(0, 0, 0, 127), outline=(235, 190, 63, 127))
    draw.rectangle((left_box_tl, left_box_br), fill=(0, 0, 0, 127), outline=(235, 190, 63, 127))
    draw.rectangle((right_box_tl, right_box_br), fill=(0, 0, 0, 127), outline=(235, 190, 63, 127))
    
    # draw text
    draw.text(dynamic_text_loc, dynamic_gesture, font=font)
    draw.text(left_text_loc, left_gesture, font=font)
    draw.text(right_text_loc, right_gesture, font=font)
    frame = np.array(frame).astype(np.uint8)

    cv2.imshow(name, frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    i += 1

# finish all jobs
jesture_runner.stop_recognition()
cap.stop()

cv2.waitKey(1)
cv2.destroyWindow(name)
cv2.destroyAllWindows()
cv2.waitKey(1)
