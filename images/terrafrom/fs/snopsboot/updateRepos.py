#!/usr/bin/python

import os
import sys
import argparse
import json
import requests

def debug(msg):
	if args.debug:
		print "DEBUG: %s" % (msg)

def process_repo_file(filename, stack={"repos":[]}, depth=0):
	print "[updateRepos]%s Processing %s" % ((' ' * depth), filename)

	try:
		repo_file = open(filename)
	except IOError as error:
		print "[updateRepos][error] Open of file \"%s\" failed: %s" % (filename, error)
		sys.exit(1)

	try:
		repo_dict = json.load(repo_file)
	except (ValueError, NameError) as error:
		print "[updateRepos][error] JSON format error in file \"%s\": %s" % (filename, error)
		sys.exit(1)

	#debug(json.dumps(repo_dict, indent=1))

	if 'include' in repo_dict:
		for includerepo in repo_dict["include"]:
			debug("found include: %s" % includerepo)
			stack = process_repo_file("/tmp/snops-repo/images/%s/fs/etc/snopsrepo.d/%s.json" % (includerepo, includerepo), stack, depth+1)

	stack["repos"].extend(repo_dict["repos"])
	return stack


# Setup and process arguments
parser = argparse.ArgumentParser(description='Script to update f5-super-netops Container Repo List')
parser.add_argument("json", help="The JSON repo file")
parser.add_argument("-D", "--debug", help="Enable debug output", action="store_true")

args = parser.parse_args()

repos = process_repo_file(args.json)
user_repos = process_repo_file('/tmp/user_repos.json')

debug(json.dumps(repos, indent=1))

with open('/home/snops/repos.json', 'w') as out:
	json.dump(repos, out, indent=1)
