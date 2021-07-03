# python_demo

Please check out the [Install](https://github.com/jesture-ai/jesture-sdk#install) section on the main page first.

To run the Python demo (checked with Python 3 only):
1. Copy the SDK file to `jesture_sdk_python/`: `cp -r ../jesture_sdk/full_cpu.dylib ./jesture_sdk_python/`
2. Copy the `mediapipe/` folder to the current folder: `cp -r ../jesture_sdk/mediapipe/ ./`
3. Run the demo script from the current folder: `python demo.py`

**Note:** The system could request to grant access to execute the `full_cpu.dylib` file, this binary is used by the Python demo to recognize hand gestures in real-time.

## Table of Available Gestures:

| Dynamic | Static |
| :-: | :-: |
| Thumb Up :thumbsup: | OK :ok_hand: |
| Thumb Down :thumbsdown: | YEAH :v: | 
| Swipe Up | ROCK :metal: | 
| Swipe Down | ONE  | 
| Swipe Left | TWO | 
| Swipe Right | THREE | 
| Sliding Two Fingers Up | SPIDERMAN :love_you_gesture: | 
| Sliding Two Fingers Down |  | 
| Sliding Two Fingers Left |  | 
| Sliding Two Fingers Right |  | 
| Zooming Out With Two Fingers |  | 
| Zooming In With Two Fingers |  | 
| Zooming Out With Full Hand |  | 
| Zooming In With Full Hand |  | 
| Stop Sign :hand:  |  | 
| Drumming Fingers |  | 
| Shaking Hand |  | 
| Pushing Hand Away |  | 
| Pulling Hand In |  | 
| Pushing Two Fingers Away |  | 
| Pulling Two Fingers In |  | 