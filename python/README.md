# python_demo

Please check out the [Install](https://github.com/jesture-ai/jesture-sdk#install) section on the main page first.

To run the Python demo (checked with Python 3 only):
1. Copy the SDK file to `jesture_sdk_python/`: `cp ../jesture_sdk/full_cpu.dylib ./jesture_sdk_python/`
2. Copy the `mediapipe` folder to the current folder: `cp -r ../jesture_sdk/mediapipe ./`
3. Run the demo script from the current folder: `python demo.py`

**Note:** The system could request to grant access to execute the `full_cpu.dylib` file, this binary is used by the Python demo to recognize hand gestures in real-time.

The result should look like this:

<img src="https://github.com/jesture-ai/jesture-sdk/blob/main/docs/gifs/python_demo.gif">

On the top there is the current dynamic gesture, on the bottom, there are the current static gestures for the left and right hand respectively. Please refer to the [list of recognized gestures](https://github.com/jesture-ai/jesture-sdk/blob/main/jesture_sdk/README.md) for more details.
