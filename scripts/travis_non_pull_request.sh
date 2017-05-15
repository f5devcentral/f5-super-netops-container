#!/bin/bash

. images/IMAGE_LIST

docker login -u $DOCKER_USER -p $DOCKER_PASS
docker images

export TAG_PREFIX=$(if [ "$BRANCH" == "master" ]; then echo ""; else echo "$BRANCH-"; fi)

for image in $IMAGE_LIST
do
	echo "Tagging $image with $DOCKER_REPO:$TAG_PREFIX$image"
	docker tag f5devcentral/f5-super-netops:$image $DOCKER_REPO:$TAG_PREFIX$image
done

docker images

for image in $IMAGE_LIST
do
	echo "Pushing $DOCKER_REPO:$TAG_PREFIX$image"
	docker push $DOCKER_REPO:$TAG_PREFIX$image
done
