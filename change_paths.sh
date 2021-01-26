JESTURE_SDK_ROOT="/Users/izakharkin/Desktop/jesture_sdk"

declare -a StringArray=("dnn" "calib3d" "features2d" "highgui" "video" "videoio" "imgcodecs" "imgproc" "core" )

for val in ${StringArray[@]}; do
        sudo install_name_tool -rpath \
		/usr/local/Cellar/opencv@3/3.4.10_4/lib \
		/usr/local/Cellar/jestureai/opencv@3/3.4.10_4/lib \
		${JESTURE_SDK_ROOT}/third_party/opencv@3/3.4.10_4/lib/libopencv_${val}.3.4.dylib
	sudo install_name_tool -id \
		/usr/local/opt/jestureai/opencv@3/lib/libopencv_${val}.3.4.dylib \
		${JESTURE_SDK_ROOT}/third_party/opencv@3/3.4.10_4/lib/libopencv_${val}.3.4.dylib
done
