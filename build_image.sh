#!/bin/bash

if [ ! -d "images/$1" ]; then
	echo "ERROR: Directory images/$1 does not exist"
	exit 1
fi

echo ""
echo "========================================================="
echo "Building image: $1"
echo "========================================================="
echo ""

cd images/$1
docker build -t f5devcentral/f5-super-netops:$1 .
