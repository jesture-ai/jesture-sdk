MEDIAPIPE_ROOT="/Users/izakharkin/Desktop/mediapipe"
JESTURE_SDK_ROOT="/Users/izakharkin/Desktop/jesture_sdk"

BIN_NAME="$1"
PATH_TO_BIN="$MEDIAPIPE_ROOT/bazel-bin/mediapipe/examples/desktop/holistic_tracking/$BIN_NAME"

echo "--- Building the target SDK binary file... ---"
echo "> Changing dir to $MEDIAPIPE_ROOT"
cd ${MEDIAPIPE_ROOT}
bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --copt="-DENABLE_DRAFTS=OFF" \
mediapipe/examples/desktop/holistic_tracking:$BIN_NAME

echo "--- Copying binary to the target dir... ---"
echo "> Changing dir to $JESTURE_SDK_ROOT"
cd ${JESTURE_SDK_ROOT}
echo "> Copying $PATH_TO_BIN to $JESTURE_SDK_ROOT"
cp ${PATH_TO_BIN} ${JESTURE_SDK_ROOT}

echo "--- Correcting paths to onnxruntime shared libraries... ---"
sudo install_name_tool -change \
	@rpath/libonnxruntime.1.3.0.dylib \
	/usr/local/opt/jestureai/onnxruntime@1.3/lib/libonnxruntime.1.3.0.dylib \
	${JESTURE_SDK_ROOT}/$BIN_NAME

echo "--- Correcting paths to opencv shared libraries... ---"
declare -a StringArray=("dnn" "calib3d" "features2d" "highgui" "video" "videoio" "imgcodecs" "imgproc" "core" )
for val in ${StringArray[@]}; do
   sudo install_name_tool -change /usr/local/opt/opencv@3/lib/libopencv_${val}.3.4.dylib \
	/usr/local/opt/jestureai/opencv@3/lib/libopencv_${val}.3.4.dylib \
	${JESTURE_SDK_ROOT}/$BIN_NAME
done

echo "--- Correcting ID of the binary... ---"
install_name_tool -id "$BIN_NAME" ${JESTURE_SDK_ROOT}/$BIN_NAME
