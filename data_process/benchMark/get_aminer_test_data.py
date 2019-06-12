#-*-coding:utf-8-*-

import sys
import random

source_file = sys.argv[1]
dest_file = sys.argv[2]

with open(source_file, mode="r") as source, open(dest_file, mode="w") as dest:
	for line in source:
		if random.randint(0, 9) == 0:
			dest.write(line)