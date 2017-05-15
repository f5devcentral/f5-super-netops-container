#!/bin/bash

. images/IMAGE_LIST

for image in $IMAGE_LIST
do
	./build_image.sh $image
	if [ $? -ne 0 ]; then
    	echo "ERROR: Build of image '$image' failed, stopping"
    	exit 1
	fi
done

echo ""
echo "All images built successfully"

exit 0
