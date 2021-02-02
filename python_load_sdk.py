import sys, platform
import ctypes, ctypes.util

import threading
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')


mylib_path = ctypes.util.find_library("full_cpu")
if not mylib_path:
    print("Unable to find the specified library.")
    sys.exit()

try:
    jesture_lib = ctypes.CDLL(mylib_path)
except OSError:
    print("Unable to load the system C library")
    sys.exit()
    
    
create_full_cpu = jesture_lib.CreateFullCpu
create_full_cpu.argtypes = [ctypes.c_int]
create_full_cpu.restype = ctypes.POINTER(ctypes.c_int)

run_full_cpu = jesture_lib.RunFullCpu
run_full_cpu.argtypes = [ctypes.POINTER(ctypes.c_int)]
run_full_cpu.restype = None

test_dispose = jesture_lib.DisposeFullCpu
test_dispose.argtypes = [ctypes.POINTER(ctypes.c_int)]
test_dispose.restype = None

get_dynamic_gesture = jesture_lib.GetCurrentDynamicGesture
get_dynamic_gesture.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_dynamic_gesture.restype = ctypes.c_char_p

get_static_left_gesture = jesture_lib.GetCurrentStaticLeftGesture
get_static_left_gesture.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_static_left_gesture.restype = ctypes.c_char_p

get_static_right_gesture = jesture_lib.GetCurrentStaticRightGesture
get_static_right_gesture.argtypes = [ctypes.POINTER(ctypes.c_int)]
get_static_right_gesture.restype = ctypes.c_char_p

# get_hand_left_keypoints = jesture_lib.GetCurrentHandLeftKeypoints
# get_hand_left_keypoints.argtypes = [ctypes.POINTER(ctypes.c_int)]
# get_hand_left_keypoints.restype = [ctypes.POINTER(ctypes.c_float)]

# get_hand_right_keypoints = jesture_lib.GetCurrentHandRightKeypoints
# get_hand_right_keypoints.argtypes = [ctypes.POINTER(ctypes.c_int)]
# get_hand_right_keypoints.restype = [ctypes.POINTER(ctypes.c_float)]

instance = create_full_cpu(0)
print(instance)


def daemon():
    logging.debug('Starting')
    run_full_cpu(instance)
    logging.debug('Exiting')


if __name__ == "__main__":
#     instance = create_full_cpu(0)
#     print(instance)
    
#     run_full_cpu(instance)

    d = threading.Thread(name='daemon', target=daemon)
    d.setDaemon(True)
    d.start()
    
    i = 0
    while (True):
        print('Dynamic gesture:', get_dynamic_gesture(instance))
        print('Static left gesture:', get_static_left_gesture(instance))
        print('Static right gesture:', get_static_right_gesture(instance))
        i += 1
        
    test_dispose(instance)
    