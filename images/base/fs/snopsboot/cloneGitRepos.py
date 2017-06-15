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

def safe_open(fn, mode='r'):
	try:
		fh = open(fn, mode)
	except IOError as e:
		print "Open of file '{0}' failed({1}): {2}".format(args[0], e.errno, e.strerror)
		sys.exit(1)

	return fh

# Setup and process arguments
parser = argparse.ArgumentParser(description='Script to clone git repos')
parser.add_argument("-f", "--filename", default="/home/snops/repos.json", help="The JSON repo file")
parser.add_argument("-D", "--debug", help="Enable debug output", action="store_true")

args = parser.parse_args()

print "[cloneGitRepos] Loading repositories from %s" % (args.filename)

repo_file = safe_open(args.filename)

try:
	repo_dict = json.load(repo_file)
except (ValueError, NameError) as error:
	print "[cloneGitRepos][error] JSON format error in file \"%s\": %s" % (args.filename, error)
	sys.exit(1)

debug(json.dumps(repo_dict, indent=1))

numrepos = len(repo_dict["repos"])
print "[cloneGitRepos] Found %s repositories to clone..." % numrepos

log = safe_open('/home/snops/log/cloneGitRepos.log', 'a')

for i in range(0, numrepos):
	obj = repo_dict["repos"][i]
	prefix = "[cloneGitRepos][%s/%s]" % (i+1, numrepos)
	if 'skip' in obj and obj["skip"]:
		print "%s Skipping %s#%s" % (prefix, obj["name"], obj["branch"])
		continue

	if 'localdir' not in obj:
		obj["localdir"] = '/home/snops/%s' % obj["name"]

	if type(obj["branch"]) is dict:
		if 'env' in obj["branch"] and obj["branch"]["env"] in os.environ:
			obj["branch"] = os.environ.get(obj["branch"]["env"])
		elif 'default' in obj["branch"]:
			obj["branch"] = obj["branch"]["default"]
		else:
			obj["branch"] = "master"

	if os.path.isdir(obj["localdir"]):
		print "%s Pulling %s#%s from %s" % (prefix, obj["name"], obj["branch"], obj["repo"])
		exitcode = call(['git','pull'], shell=False, stdout=log, stderr=log, cwd=obj["localdir"])
		if exitcode > 0:
			print "ERROR: Pull of %s failed, exiting..." % obj["name"]
			sys.exit(1)
	else:
		print "%s Cloning %s#%s from %s" % (prefix, obj["name"], obj["branch"], obj["repo"])
		gitcmd = 'git clone -b %s %s %s' % (obj["branch"], obj["repo"], obj["localdir"])
		debug("gitcmd=%s" % gitcmd)
		exitcode = call(gitcmd.split(), shell=False, stdout=log, stderr=log)
		if exitcode > 0:
			print "ERROR: Clone of %s failed, exiting..." % obj["name"]
			sys.exit(1)

	if 'skipinstall' in obj and obj['skipinstall']:
		print "%s  Skipping install" % (prefix)
		continue

	install_fn = '%s/snops_install.sh' % obj["localdir"]

	if 'install' in obj and len(obj['install']) > 0:
			install_script = safe_open(install_fn, 'w')

			for line in obj['install']:
				install_script.write("%s\n" % line)

			install_script.write('\n')
			install_script.close()

	if os.path.exists(install_fn):
		os.chmod(install_fn, 0755)
		install_log = safe_open('%s/repo_install.log' % obj["localdir"], 'a')
		print "%s  Installing %s#%s" % (prefix, obj["name"], obj["branch"])
		exitcode = call(['/bin/bash','-c','%s/snops_install.sh' % obj["localdir"]], shell=False, stdout=install_log, stderr=install_log, cwd=obj["localdir"])
		install_log.close()
		if exitcode > 0:
			print "ERROR: Install of %s failed(%s), exiting..." % (obj["name"], exitcode)
			sys.exit(1)

	i += 1

done = open('/snopsboot/SNOPS_ENV', 'a')
done.write('SNOPS_CLONE_DONE=1\n')
done.close()
