declare -a StringArray=("dnn" "calib3d" "features2d" "highgui" "video" "videoio" "imgcodecs" "imgproc" "core" )
for val in ${StringArray[@]}; do
   cp /usr/local/opt/jestureai/opencv@3/lib/libopencv_${val}.3.4.dylib ./
done
