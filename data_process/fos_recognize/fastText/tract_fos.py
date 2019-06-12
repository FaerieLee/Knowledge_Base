# -*-coding:utf-8-*-

import json
import sys
import os

map_file = "./map.txt"

fos_set = set()
source_path = sys.argv[1]
dest_path = sys.argv[2]

with open(map_file, mode="r") as reader:
	for line in reader:
		fos_set.add(json.load(line)['name'])


with open(source_path, mode="r") as r, open(dest_path, mode="w") as w:
	for line in r:
		elements = json.loads(line)
		for fos in elements['fos']:
			if fos in fos_set:
				tmp = dict()
				tmp['fos'] = fos
				if 'tile' in elements:
					tmp['title'] = elements['title']
				if 'abstract' in elements:
					tmp['abstract'] = elements['abstract']
				if 'keywords' in elements:
					tmp['keywords'] = elements['keywords']
				w.write(json.dumps(tmp) + os.linesep)
				break
