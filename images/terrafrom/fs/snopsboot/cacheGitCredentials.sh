#!/bin/bash

CWD=`pwd`


if [ -z $SNOPS_GIT_USERNAME ]; then
	exit 0
fi

if [ -z $SNOPS_GIT_HOST ]; then
	exit 0
fi

STR1=$SNOPS_GIT_USERNAME

if [ ! -z $SNOPS_GIT_PASSWORD ]; then
	STR1="$STR1:$SNOPS_GIT_PASSWORD"
fi

echo "[cacheGitCredentials] cached $SNOPS_GIT_USERNAME@$SNOPS_GIT_HOST"
su - snops -c "echo \"https://$STR1@$SNOPS_GIT_HOST\" > /home/snops/.git-credentials"
su - snops -c "chmod 400 /home/snops/.git-credentials"
su - snops -c "git config --global credential.helper 'store --file ~/.git-credentials'"

cd $CWD
