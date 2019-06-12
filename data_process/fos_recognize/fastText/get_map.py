#-*-coding:utf-8-*-

import json
import sys
import os

corpus_path = sys.argv[1]
fos_path = sys.argv[2]

fos_set = set()

with open(corpus_path, mode="r") as r, open(fos_path, mode="w") as fos_w:
	for line in r:
		elements = json.loads(line)
		fos_set.add(elements['fos'])

	iteration = 0
	for fos in fos_set:
		tmp = dict()
		tmp['id'] = iteration
		tmp['name'] = fos
		iteration += 1
		fos_w.write(json.dumps(tmp) + os.linesep)
