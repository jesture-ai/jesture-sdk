from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import argparse
import datetime
import pickle
import time
import cv2
import sys
import os

sys.path.append(os.path.abspath(".."))

from src.utils import load_image_with_alpha, overlay_alpha
from src.utils import draw_text, draw_multiline_text, draw_skeleton
from src.thread_camera_draw import ThreadCameraDraw

from jesture_sdk_python.jesture_sdk_python import JestureSdkRunner

print('cv2.__version__:', cv2.__version__)  # 4.1.2 recommended


# pasrse args
parser = argparse.ArgumentParser(description='Collect hand keypoints data for gesture recognition fitting.')
parser.add_argument('--cam_id', type=int, default=1)
args = parser.parse_args()


# create the application window
name = 'RSL: gesture collection tool'
width, height = (640, 480)
cv2.namedWindow(name)
# cv2.resizeWindow(name, (width, height))
cv2.startWindowThread()

# set the data file
data_dir = './out_data'
os.makedirs(data_dir, exist_ok=True)
now = datetime.datetime.now()
dt = f'{now.day:02d}{now.month:02d}{now.year%100:02d}_{now.hour:02d}_{now.minute:02d}'
data_file_name = f'{data_dir}/rsl_hand_keypoints_{dt}.pkl'

# set the logo stuff
logo_path = 'images/jesture_logo.png'
logo_img, logo_alpha = load_image_with_alpha(logo_path, remove_borders=True)
logo_loc = (10, 10)

# set the gestures help stuff
key_to_idx = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
              '6': 6, '7': 7, '8': 8, '9': 9, 'f': 10, 'z': 11}
key_ords = [ord(x) for x in key_to_idx]
idx_to_gesture = {0: 'а', 1: 'б', 2: 'в', 3: 'г', 4: 'е', 5: 'ж', 
                  6: 'и', 7: 'л', 8: 'м', 9: 'н', 10: 'я', 11: 'no_gesture'}
idx_to_count = {k: 0 for k in idx_to_gesture}
# help_textlist = [f'{k}: {idx_to_gesture[key_to_idx[k]]} {idx_to_count[key_to_idx[k]]}' for k in key_to_idx]
# help_textlist_str = '\n'.join(help_textlist)

help_box_width = 175
help_box_tl = {'right': (10, height//5+10), 
               'left': (width-help_box_width, height//5+10)}
help_box_br = {'right': (10+help_box_width, height-30), 
               'left': (width, height-30)}
help_text_loc = {'right': (help_box_tl['right'][0]+10, help_box_tl['right'][1]+10),
                 'left': (help_box_tl['left'][0]+10, help_box_tl['left'][1]+10)}
help_font = ImageFont.truetype("fonts/Comfortaa-Light.ttf", 20)

# set the scaled hands stuff
mid_hand_box_tl = (width//3, height-height//5)
mid_hand_box_br = (2*width//3, height)
hand_box_tl = {'right': (2*width//3, height-height//5),
               'left': (0, height-height//5)}
hand_box_br = {'right': (width, height),
               'left': (width//3, height)}

# set the hand type stuff
handtype_text = {"right": "Right hand capture (L/R)", 
                 "left": "Left hand capture (L/R)"}
handtype_text_loc = (width//2, 25)

# set the counter stuff
count_text_loc = (width//3, 25)

# set common font
font = ImageFont.truetype("fonts/Comfortaa-Light.ttf", 24)

# variables used in the main loop
pressed_duration = 0
pressed_text = ''

selfie_mode = True
hand_type = 'right'
data_list = []
prev_k = ''
i = 0


if __name__ == "__main__":
    # start Jesture SDK Python runner
    jesture_runner = JestureSdkRunner(cam_id=args.cam_id)
    jesture_runner.start_recognition()
    time.sleep(3)
    
    # start reading frames to display in the application window
    cap = ThreadCameraDraw(
        jesture_runner, cam_id=args.cam_id, width=width, height=height,
        hand_box_tl=mid_hand_box_tl, hand_box_br=mid_hand_box_br,
        draw_hand_box=False
    )
    cap.start()
    time.sleep(3)

    # start the main loop
    while(True):
        if cap.frame is None:
            continue

        # get current webcam image with drawn hand skeletons
        frame = cap.frame[:,::-1,:] if selfie_mode else cap.frame

        # draw logo
#         frame = overlay_alpha(logo_img[:,:,::-1], logo_alpha, frame, loc=logo_loc, alpha=1.0)

        # draw ui elements
        frame = Image.fromarray(frame if type(np.array([])) == type(frame) else frame.get())
        draw = ImageDraw.Draw(frame, "RGBA")
        draw.rectangle((help_box_tl[hand_type], help_box_br[hand_type]), 
                       fill=(0, 0, 0, 127), outline=(235, 190, 63, 255))
        # draw.rectangle((hand_box_tl, hand_box_br), fill=(0, 0, 0, 127), outline=(235, 190, 63, 255))

        # draw text
        draw.multiline_text(handtype_text_loc, handtype_text[hand_type], 
                            font=font, fill=(255, 255, 255, 200))

        help_textlist = [f'{idx_to_count[key_to_idx[k]]} | {k}: {idx_to_gesture[key_to_idx[k]]}' 
                         for k in key_to_idx]
        help_textlist_str = '\n'.join(help_textlist)
        draw.multiline_text(help_text_loc[hand_type], help_textlist_str, 
                            font=help_font, fill=(255, 255, 255))

        # retrieve keyboard signal
        c = cv2.waitKey(1) % 256
        if c == ord('q'):
            break

        if c == ord('l'):
            hand_type = 'left'
        if c == ord('r'):
            hand_type = 'right'

        # retrieve if gesture key is pressed
        if chr(c) in key_to_idx:
            k, v = chr(c), idx_to_gesture[key_to_idx[chr(c)]]
            pressed_text = f'{idx_to_count[key_to_idx[k]]} | {k}: {v}'
            idx_to_count[key_to_idx[k]] += 1
            pressed_duration = 4
            print(f"pressed {pressed_text}, shape: {frame.size}")
            data_list.append({
                'hand_type': hand_type,
                'gesture_id': key_to_idx[k],
                'gesture_name': v,
                'pred_gesture_name': jesture_runner.get_gesture(
                    f'{hand_type}_static'),
                'keypoints': jesture_runner.get_hand_keypoints(
                    f'{hand_type}_keypoints'),
                'scaled_keypoints': jesture_runner.get_hand_keypoints(
                    f'scaled_{hand_type}_keypoints'),
            })
            # save current data to not to lose it 
            # in case if the program accidentally exited
            if k != prev_k:
                with open(data_file_name, 'wb') as file:
                    pickle.dump(data_list, file)
            prev_k = k

        # draw notification text if key was pressed less then 12 frames ago
        if pressed_duration > 0:
            notify_textlist_str = "\n".join(
                [x if x == pressed_text else "" for x in help_textlist])
            draw.multiline_text(help_text_loc[hand_type], notify_textlist_str, 
                                font=help_font, fill=(235, 190, 63))
            pressed_duration -= 1

        frame = np.array(frame).astype(np.uint8)
        cv2.imshow(name, frame)

        i += 1

    # save all data collected
    with open(data_file_name, 'wb') as file:
        print(f'Dumping {len(data_list)} items to {data_file_name}...')
        pickle.dump(data_list, file)
        print(f'Dumped.')

    # finish and close all resources
    cap.stop()
    jesture_runner.stop_recognition()

    cv2.waitKey(1)
    cv2.destroyWindow(name)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
