# Jesture SDK: Python

Please check out the [Install](https://github.com/jesture-ai/jesture-sdk#install) section on the main page first.

## Demo

To run the Python demo (checked with Python 3 only):
1. Copy the SDK file to `jesture_sdk_python/`: `cp ../jesture_sdk/full_cpu.dylib ./jesture_sdk_python/`
2. Copy the `mediapipe` folder to the current folder: `cp -r ../jesture_sdk/mediapipe ./`
3. Run the demo script from the current folder: `python demo.py`

**Note:** The system could request to grant access to execute the `full_cpu.dylib` file, this binary is used by the Python demo to recognize hand gestures in real-time.

<img src="https://github.com/jesture-ai/jesture-sdk/blob/main/docs/gifs/python_demo.gif">

On the top there is the current dynamic gesture, on the bottom, there are the current static gestures for the left and right hand respectively. Please refer to the [list of recognized gestures](https://github.com/jesture-ai/jesture-sdk/blob/main/jesture_sdk/README.md) for more details.

## Annotation tool

One can use our SDK to collect the hand keypoints to further train a gesture recognition model. We prepared a convenient script for this:

```
pyton annotation.py --cam_id=0
```
**Note:** You need to do steps 1 and 2 from the Demo instructions to be able to use the SDK python wrapper. 

<img src="https://github.com/jesture-ai/jesture-sdk/blob/main/docs/gifs/python_annotation_large.gif">

Each time when a key ("0"-"9" in this case) is pressed the record is added to a dict and it is saved to `out_data/hand_keypoints_{datatime}.pkl` file.

Feel free to change the corresponding keys (`key_to_idx`) and the class names (`idx_to_gesture`) in `annotation.py`.
