#!/bin/bash

if [ $SNOPS_AUTOCLONE == "0" ]; then
	echo "[cloneGitRepos] Skipping..."
	exit 0
fi

CWD=`pwd`

cd /home/snops
mkdir -p /home/snops/log

if [ ! -f "/home/snops/repos" ]; then
	echo "[cloneGitRepos] Retrieving repository list from ${SNOPS_GH_BRANCH}"
	curl -s -o /home/snops/repos https://raw.githubusercontent.com/f5devcentral/f5-super-netops-container/${SNOPS_GH_BRANCH}/snops.repos
fi

NUMREPOS=`wc -l /home/snops/repos | cut -d' ' -f1`
I=1

echo "[cloneGitRepos] Found $NUMREPOS repositories to clone..."
for i in `cat /home/snops/repos`
do
 REPO=`echo $i | cut -d';' -f1`
 REPOURL=`echo $i | cut -d';' -f2`
 BRANCH=`echo $i | cut -d';' -f3`
 echo "[cloneGitRepos][$I/$NUMREPOS] Cloning $REPO:$BRANCH from $REPOURL"
 git clone -b $BRANCH $REPOURL >> /home/snops/log/cloneGitRepos.log 2>&1
 if [ -f "/snopsboot/repo_install/$REPO" ]; then
  echo "[cloneGitRepos][$I/$NUMREPOS]  Installing $REPO:$BRANCH..."
  cd /home/snops/$REPO && /snopsboot/repo_install/$REPO >> /home/snops/$REPO/repo_install.log 2>&1
 fi
 let I+=1
 cd /home/snops
done

cd $CWD
