#!/bin/bash

INSTALL_DIR=/usr/local/Cellar/jestureai/
LINK_DIR=/usr/local/opt/jestureai/

if [ ! -d "$INSTALL_DIR" ]; then
	mkdir ${INSTALL_DIR}
fi
if [ ! -d "$LINK_DIR" ]; then
        mkdir ${LINK_DIR}
fi

# ------------ INSTALL OPENCV -------------

# Note: Version 3.4.10 is well-tested. Newer versions will probably also work.
OPENCV_ARCHIVE_PATH=third_party/opencv@3.zip

tar -xvzf ${OPENCV_ARCHIVE_PATH} -C ${INSTALL_DIR}

# Note: Mandatory step, this path is required by jesture_sdk.dylib.
ln -s ${INSTALL_DIR}/opencv@3/3.4.10_4/ ${LINK_DIR}/opencv@3

# ------------ INSTALL ONNXRUNTIME -------------

# Note: Version 1.3 because newer releases have some issues with CPU load on macOS.
ORT_ARCHIVE_PATH=third_party/onnxruntime@1.3.zip

tar -xvzf ${ORT_ARCHIVE_PATH} -C ${INSTALL_DIR}

# Note: Mandatory step, this path is required by jesture_sdk.dylib.
ln -s ${INSTALL_DIR}/onnxruntime@1.3/ ${LINK_DIR}/onnxruntime@1.3
