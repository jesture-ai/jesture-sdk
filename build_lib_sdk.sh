MEDIAPIPE_ROOT="/Users/izakharkin/Desktop/mediapipe"
JESTURE_SDK_ROOT="/Users/izakharkin/Desktop/jesture_sdk"

BIN_NAME="full_cpu.dylib"
PATH_TO_BIN="$MEDIAPIPE_ROOT/bazel-bin/mediapipe/examples/desktop/holistic_tracking/$BIN_NAME"

# --- Build the target SDK binary file ---

cd ${MEDIAPIPE_ROOT}
bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --copt="-DENABLE_DRAFTS=OFF" \
mediapipe/examples/desktop/holistic_tracking:$BIN_NAME

# --- Copy binary to the target dir ---

cd ${JESTURE_SDK_ROOT}
cp ${PATH_TO_BIN} ${JESTURE_SDK_ROOT}

# --- Correct paths to onnxruntime shared libraries ---

sudo install_name_tool -change \
	@rpath/libonnxruntime.1.3.0.dylib \
	/usr/local/opt/jestureai/onnxruntime@1.3/lib/libonnxruntime.1.3.0.dylib \
	${JESTURE_SDK_ROOT}/$BIN_NAME

#sudo install_name_tool -rpath \
#	@loader_path/../../../../_solib_darwin_x86_64/_U@macos_Uonnxruntime_S_S_Connxruntime___Umacos_Uonnxruntime_Slib \
#	/usr/local/opt/jestureai/onnxruntime@1.3 \
#	${JESTURE_SDK_ROOT}/$BIN_NAME

# --- Correct paths to opencv shared libraries ---

declare -a StringArray=("dnn" "calib3d" "features2d" "highgui" "video" "videoio" "imgcodecs" "imgproc" "core" )
for val in ${StringArray[@]}; do
   sudo install_name_tool -change /usr/local/opt/opencv@3/lib/libopencv_${val}.3.4.dylib \
	/usr/local/opt/jestureai/opencv@3/lib/libopencv_${val}.3.4.dylib \
	${JESTURE_SDK_ROOT}/$BIN_NAME
done

#sudo install_name_tool -rpath \
#	@loader_path/../../../../_solib_darwin_x86_64/_U@macos_Uopencv_S_S_Copencv___Umacos_Uopencv_Slib \
#	/usr/local/opt/jestureai/opencv@3/lib \
#	${JESTURE_SDK_ROOT}/$BIN_NAME
