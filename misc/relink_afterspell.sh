BIN_NAME="$1"
PATH_TO_BIN="/Users/izakharkin/Desktop/deepjest/unijest/versus/MagestyMVP/Afterspell/PlugIns/$BIN_NAME"

echo "--- Correcting paths to onnxruntime shared libraries... ---"
sudo install_name_tool -change \
	/usr/local/opt/jestureai/onnxruntime@1.3/lib/libonnxruntime.1.3.0.dylib \
	@executable_path/../Frameworks/libonnxruntime.1.3.0.dylib \
	${PATH_TO_BIN}

echo "--- Correcting paths to opencv shared libraries... ---"
declare -a StringArray=("dnn" "calib3d" "features2d" "highgui" "video" "videoio" "imgcodecs" "imgproc" "core" )
for val in ${StringArray[@]}; do
   sudo install_name_tool -change \
	/usr/local/opt/jestureai/opencv@3/lib/libopencv_${val}.3.4.dylib \
	@executable_path/../Frameworks/libopencv_${val}.3.4.dylib \
	${PATH_TO_BIN}
done

