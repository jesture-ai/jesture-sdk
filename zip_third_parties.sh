JESTURE_SDK_ROOT="/Users/izakharkin/Desktop/jesture_sdk"

cd ${JESTURE_SDK_ROOT}/third_party/

for dir in ./*/
do
        dir=${dir%*/}      # remove the trailing "/"
#        echo ${dir##*/}    # print everything after the final "/"
	zip -r ${dir}.zip ${dir}
done
