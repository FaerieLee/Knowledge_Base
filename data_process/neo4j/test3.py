#-*-coding:utf-8-*-

import sys

file_path = sys.argv[1]
destination_file = sys.argv[2]

with open(file_path) as reader, open(destination_file, mode ="w") as writer:
	for line in reader:
		if len(line.split(',')) < 2:
			writer.write(line)
