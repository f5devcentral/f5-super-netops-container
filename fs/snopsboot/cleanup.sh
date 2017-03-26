/snopsboot/cleanGitRepos.sh
su - snops -c "npm cache clean"
su - snops -c "rm -Rf /home/.cache/pip"
rm -f /home/log/*
npm cache clean
rm -Rf /root/.cache/pip
