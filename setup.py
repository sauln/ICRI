#!/usr/bin/env python

print("setup ICRI project")
import os
import db.setup

print("build interim storage dirs")
dirs = 'data/solutions/search'
if not os.path.isdir(dirs):
	os.makedirs(dirs)















