#!/usr/bin/python

import os
import sys
import argparse
import json
from subprocess import call

# cd /home/snops
# mkdir -p /home/snops/log

def debug(msg):
	if args.debug:
		print "DEBUG: %s" % (msg)

# Setup and process arguments
parser = argparse.ArgumentParser(description='Script to clone git repos')
parser.add_argument("-f", "--filename", default="/home/snops/repos.json", help="The JSON repo file")
parser.add_argument("-D", "--debug", help="Enable debug output", action="store_true")

args = parser.parse_args()

print "[cloneGitRepos] Loading repositories from %s" % (args.filename)

try:
	repo_file = open(args.filename)
except IOError as error:
	print "[cloneGitRepos][error] Open of file \"%s\" failed: %s" % (args.filename, error)
	sys.exit(1)

try:
	repo_dict = json.load(repo_file)
except (ValueError, NameError) as error:
	print "[clo][error] JSON format error in file \"%s\": %s" % (args.filename, error)
	sys.exit(1)

debug(json.dumps(repo_dict, indent=1))

numrepos = len(repo_dict["repos"])
print "[cloneGitRepos] Found %s repositories to clone..." % numrepos

try:
    log = open('/home/snops/log/cloneGitRepos.log', 'a')
except IOError as e:
   print "Open of log file failed({0}): {1}".format(e.errno, e.strerror)
   sys.exit(1)

for i in range(0, numrepos):
	obj = repo_dict["repos"][i]
	prefix = "[cloneGitRepos][%s/%s]" % (i+1, numrepos)
	if 'skip' in obj and obj["skip"]:
		print "%s Skipping %s#%s" % (prefix, obj["name"], obj["branch"])
		continue

	localdir = '/home/snops/%s' % obj["name"]
	if os.path.isdir(localdir):
		print "%s Pulling %s#%s from %s" % (prefix, obj["name"], obj["branch"], obj["repo"])
		exitcode = call(['git','pull'], shell=False, stdout=log, stderr=log, cwd=localdir)
		if exitcode > 0:
			print "ERROR: Pull of %s failed, exiting..." % obj["name"]
			sys.exit(1)
	else:
		print "%s Cloning %s#%s from %s" % (prefix, obj["name"], obj["branch"], obj["repo"])
		gitcmd = 'git clone -b %s %s %s' % (obj["branch"], obj["repo"], localdir)
		debug("gitcmd=%s" % gitcmd)
		exitcode = call(gitcmd.split(), shell=False, stdout=log, stderr=log)
		if exitcode > 0:
			print "ERROR: Clone of %s failed, exiting..." % obj["name"]
			sys.exit(1)

	if 'skipinstall' in obj and obj['skipinstall']:
		print "%s  Skipping install" % (prefix)
		continue

	if os.path.exists(os.path.join(os.path.sep, 'snopsboot','repo_install',obj["name"])):
		try:
		    install_log = open('/home/snops/%s/repo_install.log' % obj["name"], 'a')
		except IOError as e:
		   print "Open of install log file failed({0}): {1}".format(e.errno, e.strerror)
		   sys.exit(1)

		print "%s  Installing %s#%s" % (prefix, obj["name"], obj["branch"])
		exitcode = call(['/snopsboot/repo_install/%s' % obj["name"]], shell=False, stdout=install_log, stderr=install_log, cwd=localdir)
		install_log.close()
		if exitcode > 0:
			print "ERROR: Install of %s failed(%s), exiting..." % (obj["name"], exitcode)
			sys.exit(1)

	i += 1

