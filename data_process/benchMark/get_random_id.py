#-*-coding:utf-8-*-

import sys
import random


if __name__ == '__main__':

	file_path = sys.argv[1]
	destination_file = sys.argv[2]

	with open(destination_file, mode="w", encoding="utf-8") as dtnf, \
			open(file_path, mode="r", encoding="utf-8") as source:
		for line in source:
			if random.uniform(0,1) > 0.95:
				dtnf.write(line)

