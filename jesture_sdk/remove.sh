#!/bin/bash
#
# Copyright (c) Jesture AI Inc. All rights reserved.
#
# See the license details in LICENSE.md.
#

INSTALL_DIR=/usr/local/Cellar/jestureai/
LINK_DIR=/usr/local/opt/jestureai/

if [ -d "$INSTALL_DIR" ]; then
        rm -r ${INSTALL_DIR}
fi
if [ -d "$LINK_DIR" ]; then
        rm -r ${LINK_DIR}
fi

