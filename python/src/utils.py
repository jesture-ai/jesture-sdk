from PIL import Image
import numpy as np
import cv2


def to_np(pil_img):
    return np.array(pil_img)[...,None]


def load_image_with_alpha(img_path, resize_rate=10, remove_borders=False):
    img = Image.open(img_path, 'r')
    has_alpha = img.mode == 'RGBA'
    assert(has_alpha)
    
    red, green, blue, alpha = img.split()
    
    img_rgb = np.concatenate([to_np(red), to_np(green), to_np(blue)], axis=-1)
    img_alpha = to_np(alpha)
    
    if remove_borders:
        bsize = 250
        print(f'Removing {bsize} pixels from up and down borders')
        img_rgb = img_rgb[bsize:-bsize, :, :]
        img_alpha = img_alpha[bsize:-bsize, :, :]
    
    orig_size = (img_rgb.shape[1], img_rgb.shape[0])
    print('Original image size:', orig_size)
    target_size = (orig_size[0] // resize_rate, orig_size[1] // resize_rate)
    print('Target size:', target_size)
        
    img_rgb = cv2.resize(img_rgb, target_size)
    img_alpha = cv2.resize(img_alpha, target_size)

    return img_rgb, img_alpha


def blur_image_patch(image, xmin, ymin, xmax, ymax, num_iter=5):
    patch = image[ymin:ymax, xmin:xmax, :]
    for i in range(num_iter):
        patch = cv2.blur(patch, (5, 5))
    image[ymin:ymax, xmin:xmax, :] = patch
    return image


def overlay_alpha(src, src_alpha, dest, loc=(0, 0), alpha=1.0):
    src_h, src_w = src.shape[:2]
    dest_h, dest_w = dest.shape[:2]
    x1, y1 = max(0, loc[0]), max(0, loc[1])
    x2, y2 = min(x1 + src_w, dest_w), min(y1 + src_h, dest_h)
    if isinstance(src_alpha, type(src)):
        srca_h, srca_w = src_alpha.shape[:2]
        assert(srca_h == src_h and srca_w == src_w)
        src_alpha = src_alpha[:,:,None] // 255
    src_mask = src_alpha * alpha
    dest_mask = 1 - src_alpha
    dest_mask[dest_mask==0] = 1 - alpha
    dest[y1:y2,x1:x2,:] = dest_mask * dest[y1:y2,x1:x2,:] + src_mask * src
    return dest


def draw_text(image, text, org=(0, 185), font=cv2.FONT_HERSHEY_SIMPLEX, 
              fontScale=1, color=(255, 255, 255), thickness=2, 
              lineType=cv2.LINE_AA, bottomLeftOrigin=False):
    image = cv2.putText(image, text, org, font, fontScale, 
                        color, thickness, lineType, bottomLeftOrigin)
    return image


def draw_multiline_text(image, textlist, height=480, width=640, xloc=10, 
                        font=cv2.FONT_HERSHEY_SIMPLEX, font_size=1.0, color=(255,255,255), 
                        font_thickness=2, lineType=cv2.LINE_AA):
    for i, line in enumerate(textlist):
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        gap = textsize[1] + 5
        y = (height//2 + textsize[1]) // 2 + i * gap
        cv2.putText(image, line, (xloc, y), font, font_size, 
                    color, font_thickness, lineType)
    return image


def draw_skeleton(image, landmarks, indices=True):
    HAND_SKELETON = {
        'palm': {0:1,1:5,5:9,9:13,13:17,17:0},
        'thumb': {1:2,2:3,3:4},
        'forefinger': {5:6,6:7,7:8},
        'middle_finger': {9:10,10:11,11:12},
        'ring_finger': {13:14,14:15,15:16},
        'pinkie': {17:18,18:19,19:20}
    }
    for hand_part_name in HAND_SKELETON:
        for curr_point in HAND_SKELETON[hand_part_name]:
            curr_point_coords = (int(landmarks[curr_point][0]), int(landmarks[curr_point][1]))
            next_point = landmarks[HAND_SKELETON[hand_part_name][curr_point]]
            next_point_coords = (int(next_point[0]), int(next_point[1]))
            cv2.line(
                image, 
                pt1=curr_point_coords,
                pt2=next_point_coords, 
                color=(255,255,255),
                thickness=2
            )
    for i, coords in enumerate(landmarks):
        if indices:
            image = cv2.putText(
                image, 
                text=str(i), 
                org=(int(coords[0]-5), int(coords[1])-10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(255,255,255)
            )
        image = cv2.circle(
            image, 
            center=(int(coords[0]), int(coords[1])), 
            radius=1, 
            color=(235, 190, 63), 
            thickness=5, 
            lineType=8, 
            shift=0
        )
    return image
