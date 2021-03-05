MEDIAPIPE_ROOT="/c/Users/USER/mediapipe-holistic"
JESTURE_SDK_ROOT="/c/Users/USER/jesture-sdk"

BIN_NAME="$1"
PATH_TO_BIN="$MEDIAPIPE_ROOT/bazel-bin/mediapipe/examples/desktop/holistic_tracking/$BIN_NAME"

echo "--- Build the target SDK binary file ---"
echo "> Changing dir to $MEDIAPIPE_ROOT"
cd ${MEDIAPIPE_ROOT}
bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --copt="-DENABLE_DRAFTS=OFF" --action_env PYTHON_BIN_PATH="C://Users//USER//AppData//Local//Programs//Python//Python37//python.exe" mediapipe/examples/desktop/holistic_tracking:$BIN_NAME

echo "--- Copy binary to the target dir ---"
echo "> Changing dir to $JESTURE_SDK_ROOT"
cd ${JESTURE_SDK_ROOT}
echo "> Copying $PATH_TO_BIN to $JESTURE_SDK_ROOT"
cp ${PATH_TO_BIN} ${JESTURE_SDK_ROOT}

# echo "--- Correct paths to onnxruntime shared libraries ---"
# sudo install_name_tool -change \
# 	@rpath/libonnxruntime.1.3.0.dylib \
# 	/usr/local/opt/jestureai/onnxruntime@1.3/lib/libonnxruntime.1.3.0.dylib \
# 	${JESTURE_SDK_ROOT}/$BIN_NAME

# echo "--- Correct paths to opencv shared libraries ---"
# declare -a StringArray=("dnn" "calib3d" "features2d" "highgui" "video" "videoio" "imgcodecs" "imgproc" "core" )
# for val in ${StringArray[@]}; do
#    sudo install_name_tool -change /usr/local/opt/opencv@3/lib/libopencv_${val}.3.4.dylib \
# 	/usr/local/opt/jestureai/opencv@3/lib/libopencv_${val}.3.4.dylib \
# 	${JESTURE_SDK_ROOT}/$BIN_NAME
# done
