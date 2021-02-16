from numpy.ctypeslib import ndpointer
import ctypes, ctypes.util
import sys, platform
import numpy as np
import shutil

from threading import Thread
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

# Mac OS X specific stuff
ctypes.util.find_library("libSystem.B.dylib")
print('shutil.which("libSystem.B.dylib"):', shutil.which("libSystem.B.dylib"))
print('ctypes.CDLL("libSystem.B.dylib")._name:', ctypes.CDLL("libSystem.B.dylib")._name)
print('ctypes.__version__:', ctypes.__version__)
print('platform.mac_ver():', platform.mac_ver())

# ------------ Jesture SDK setup ------------

jesturesdk_lib_name = "full_cpu"
jesturesdk_lib_path = ctypes.util.find_library(jesturesdk_lib_name)
if not jesturesdk_lib_path:
    print("Unable to find the specified library: {}".format(jesturesdk_lib_name))
    sys.exit()

try:
    jesture_lib = ctypes.CDLL(jesturesdk_lib_path)
except OSError:
    print("Unable to load the library from {}".format(jesturesdk_lib_path))
    sys.exit()

# -------------- COMMON --------------

create_full_cpu = jesture_lib.CreateFullCpu
create_full_cpu.argtypes = [ctypes.c_int]
create_full_cpu.restype = ctypes.POINTER(ctypes.c_int)

run_full_cpu = jesture_lib.RunFullCpu
run_full_cpu.argtypes = [ctypes.POINTER(ctypes.c_int)]
run_full_cpu.restype = None

stop_full_cpu = jesture_lib.StopFullCpu
stop_full_cpu.argtypes = [ctypes.POINTER(ctypes.c_int)]
stop_full_cpu.restype = None

dispose_full_cpu = jesture_lib.DisposeFullCpu
dispose_full_cpu.argtypes = [ctypes.POINTER(ctypes.c_int)]
dispose_full_cpu.restype = None

get_camera_width = jesture_lib.GetCameraWidth
get_camera_width.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_camera_width.restype = ctypes.c_int

get_camera_height = jesture_lib.GetCameraHeight
get_camera_height.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_camera_height.restype = ctypes.c_int

# -------------- HANDS --------------

# gestures

get_dynamic_gesture = jesture_lib.GetCurrentDynamicGesture
get_dynamic_gesture.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_dynamic_gesture.restype = ctypes.c_char_p

get_dynamic_gesture_idx = jesture_lib.GetCurrentDynamicGestureIdx
get_dynamic_gesture_idx.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_dynamic_gesture_idx.restype = ctypes.c_int

get_static_left_gesture = jesture_lib.GetCurrentStaticLeftGesture
get_static_left_gesture.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_static_left_gesture.restype = ctypes.c_char_p

get_static_right_gesture = jesture_lib.GetCurrentStaticRightGesture
get_static_right_gesture.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_static_right_gesture.restype = ctypes.c_char_p

# screensize-relative keypoints

get_hand_left_keypoints = jesture_lib.GetCurrentHandLeftKeypoints
get_hand_left_keypoints.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_hand_left_keypoints.restype = ndpointer(dtype=ctypes.c_double, shape=(63,))

get_hand_right_keypoints = jesture_lib.GetCurrentHandRightKeypoints
get_hand_right_keypoints.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_hand_right_keypoints.restype = ndpointer(dtype=ctypes.c_double, shape=(63,))

# screensize-independent keypoints

get_scaled_left_keypoints = jesture_lib.GetCurrentScaledLeftKeypoints
get_scaled_left_keypoints.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_scaled_left_keypoints.restype = ndpointer(dtype=ctypes.c_double, shape=(63,))

get_scaled_right_keypoints = jesture_lib.GetCurrentScaledRightKeypoints
get_scaled_right_keypoints.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_scaled_right_keypoints.restype = ndpointer(dtype=ctypes.c_double, shape=(63,))
        
        
class JestureSdkRunner:
    HAND_KEYPOINTS_METHOD_DICT = {
        'left_keypoints': get_hand_left_keypoints, 
        'right_keypoints': get_hand_right_keypoints, 
        'scaled_left_keypoints': get_scaled_left_keypoints, 
        'scaled_right_keypoints': get_scaled_right_keypoints, 
    }
    GESTURE_METHOD_DICT = {
        'dynamic': get_dynamic_gesture,
        'left_static': get_static_left_gesture,
        'right_static': get_static_right_gesture
    }
    
    def __init__(self, cam_id):
        self.cam_id = cam_id
        self.instance = create_full_cpu(cam_id)
        logging.debug('[JestureSdkRunner] Instance created.')

    def start_recognition(self):
        self.thread = Thread(name='jesture_sdk_python_thread', 
                             target=self.run_recognition,
                             args=())
        # d.setDaemon(True)
        self.thread.start()
        logging.debug('[JestureSdkRunner] Recognition thread started.')
        return self

    def run_recognition(self):
        logging.debug('[JestureSdkRunner] Starting recognition...')
        run_full_cpu(self.instance)

    def stop_recognition(self):
        logging.debug('[JestureSdkRunner] Stopping recognition...')
        stop_full_cpu(self.instance)
        logging.debug('[JestureSdkRunner] Recognition stopped.')
        self.thread.join()
        logging.debug('[JestureSdkRunner] Thread joined.')
        
    def get_camera_width(self):
        return get_camera_width(self.instance)
    
    def get_camera_height(self):
        return get_camera_height(self.instance)
    
    def get_gesture(self, gesture_type):
        '''
        Get hand gesture by `gesture_type`.
        '''
        
        method = JestureSdkRunner.GESTURE_METHOD_DICT[gesture_type]
        return method(self.instance).decode()

    def get_hand_keypoints(self, keypoints_type):
        '''
        Get hand keypoints by `keypoints_type`.
        '''
        
        method = JestureSdkRunner.HAND_KEYPOINTS_METHOD_DICT[keypoints_type]
        raw_keypoints = method(self.instance)
        keypoints = raw_keypoints.reshape(21, 3).copy()
        return keypoints
    