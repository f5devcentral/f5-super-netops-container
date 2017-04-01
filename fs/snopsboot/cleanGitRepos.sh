#!/bin/bash

CWD=`pwd`

cd /home
for i in `cat /home/snops/repos`
do
 REPO=`echo $i | cut -d';' -f1`
 REPOURL=`echo $i | cut -d';' -f2`
 BRANCH=`echo $i | cut -d';' -f3`
 if [ -d "/home/snops/$REPO" ]; then
  echo "[getGitRepos] Removing $REPO from /home/snops/$REPO"
  cd /home/snops/$REPO && /snopsboot/repo_install/$REPO.uninstall
  su - snops -c "rm -Rf /home/snops/$REPO"
 fi
done

cd $CWD
