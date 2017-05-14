#!/bin/bash

if [ $SNOPS_AUTOCLONE == "0" ]; then
	echo "[cloneGitRepos] Skipping..."
	exit 0
fi

CWD=`pwd`

cd /home/snops
mkdir -p /home/snops/log

if [ ! -d "/tmp/snops-repo" ]; then
	echo "[cloneGitRepos] Retrieving repository list from ${SNOPS_REPO}#${SNOPS_GH_BRANCH}"
	git clone -b $SNOPS_GH_BRANCH $SNOPS_REPO /tmp/snops-repo >> /home/snops/log/cloneGitRepos.log 2>&1
fi

python /snopsboot/updateRepos.py /tmp/snops-repo/images/$SNOPS_IMAGE/fs/etc/snopsrepo.d/$SNOPS_IMAGE.json
python /snopsboot/cloneGitRepos.py
