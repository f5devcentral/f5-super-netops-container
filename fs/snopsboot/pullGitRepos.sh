#!/bin/bash

CWD=`pwd`

cd /home
for i in `cat /home/snops/repos`
do
 REPO=`echo $i | cut -d';' -f1`
 REPOURL=`echo $i | cut -d';' -f2`
 BRANCH=`echo $i | cut -d';' -f3`
 echo "[pullGitRepos] Pulling $REPO:$BRANCH from $REPOURL"
 su - snops -c "cd /home/snops/$REPO && git pull >> /home/snops/log/pullGitRepos.log 2>&1"
 if [ -f "/snopsboot/repo_install/$REPO" ]; then
  echo "[pullGitRepos]  Re-installing $REPO:$BRANCH..."
  su - snops -c "cd /home/snops/$REPO && /snopsboot/repo_install/$REPO >> /home/snops/$REPO/repo_install.log 2>&1"
 fi
 cd /home
done

cd $CWD
