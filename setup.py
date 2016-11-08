#!/usr/bin/env python

import os
import db.setup as db

db.initialize()




dirs = 'data/solutions/search'
if not os.path.isdir(dirs):
	os.makedirs(dirs)















