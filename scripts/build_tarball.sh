#!/bin/bash
# build_tarball.sh
# Usage: build_tarball.sh file1 file2 ...
# Builds tarball, prepending DEST_PATH to filenames, for use in model deployment
# Outputs {md5}.tar.gz where {md5} is the md5sum of the tarball

set -e

DEST_PATH="app/neural_net/"
GZ_FILENAME="model.tar.gz"

tar -czvf $GZ_FILENAME --transform "s|^|DEST_PATH|g" "$@"

md5=($(md5sum $GZ_FILENAME))

mv $GZ_FILENAME "$md5".tar.gz
