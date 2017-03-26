#!/bin/bash

CWD=`pwd`

cd /home
for i in `cat /home/repos`
do
 REPO=`echo $i | cut -d';' -f1`
 REPOURL=`echo $i | cut -d';' -f2`
 BRANCH=`echo $i | cut -d';' -f3`
 echo "[pullGitRepos] Pulling $REPO:$BRANCH from $REPOURL"
 su - snops -c "cd /home/$REPO && git pull >> /home/log/pullGitRepos.log 2>&1"
 if [ -f "/snopsboot/repo_install/$REPO" ]; then
  echo "[pullGitRepos]  Re-installing $REPO:$BRANCH..."
  su - snops -c "cd /home/$REPO && /snopsboot/repo_install/$REPO >> /home/$REPO/repo_install.log 2>&1"
 fi
 cd /home
done

cd $CWD
