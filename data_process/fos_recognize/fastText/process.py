#-*-coding:utf-8-*-

import json
import sys
import random
import os

from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["172.31.34.104:9200"], timeout=5000)


def translate(article):
	results = es.indices.analyze(body={
		"analyzer": "english",
		"text": article
	}, format="text")

	result = ""
	for token in results['tokens']:
		if len(token) > 1:
			result = result + token['token'] + " "

	return result


corpus_path = sys.argv[1]
map_path = sys.argv[2]

train_o_path = sys.argv[3]
val_o_path = sys.argv[4]

train_p_path = sys.argv[5]
val_p_path = sys.argv[6]

train_original_list = []
val_original_list = []

train_participle_list = []
val_participle_list = []

name_id_map = dict()

with open(map_path, mode="r") as mr:
	for line in mr:
		elements = json.loads(line)
		name_id_map[elements['name']] = elements['id']

with open(corpus_path, mode="r") as r:
	for line in r:
		elements = json.loads(line)

		tmp = ""
		if 'title' in elements:
			tmp += elements['title']
		if 'keywords' in elements:
			for keyword in elements['keywords']:
				tmp = tmp + keyword + ' '
		if 'abstract' in elements:
			tmp += elements['abstract']

		if tmp:
			if random.random() < 0.8:
				train_original_list.append('__label__' + str(name_id_map[elements['fos']]) + ' ' + tmp)
				train_participle_list.append('__label__' + str(name_id_map[elements['fos']]) + ' ' + translate(tmp))
			else:
				val_original_list.append('__label__' + str(name_id_map[elements['fos']]) + ' ' + tmp)
				val_participle_list.append('__label__' + str(name_id_map[elements['fos']]) + ' ' + translate(tmp))


random.shuffle(train_original_list)
random.shuffle(val_original_list)

with  open(train_o_path, mode="w") as t_o_w, open(val_o_path, mode="w") as v_o_w:
	for line in train_original_list:
		t_o_w.write(line + os.linesep)

	for line in val_original_list:
		v_o_w.write(line + os.linesep)


random.shuffle(train_participle_list)
random.shuffle(val_participle_list)
with  open(train_p_path, mode="w") as t_p_w, open(val_p_path, mode="w") as v_p_w:

	for line in train_participle_list:
		t_p_w.write(line + os.linesep)

	for line in val_participle_list:
		v_p_w.write(line + os.linesep)