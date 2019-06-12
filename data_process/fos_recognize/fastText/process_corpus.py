# -*-coding:utf-8-*-

import json
import multiprocessing
import random
import os


def conversion_fast_text(corpus_path, train_set, val_set, map_path):
	train_list = []
	val_list = []

	name_id_map = dict()

	fos_set = set()

	with open(map_path, mode="r") as mr:
		for line in mr:
			elements = json.loads(line)
			name_id_map[elements['name']] = elements['id']
			fos_set.add(elements['name'])

	with open(corpus_path, mode="r") as r, open(train_set, mode="w") as t_w, open(val_set, mode="w") as v_w:
		for line in r:
			elements = json.loads(line)
			foses = set(elements['fos']) & fos_set
			labels = ''
			for fos in foses:
				labels = labels + '__label__' + str(name_id_map[fos]) + ' '
			if random.random() < 0.8:
				train_list.append(labels + elements['words'])
			else:
				val_list.append(labels + elements['words'])

		random.shuffle(train_list)
		random.shuffle(val_list)

		for line in train_list:
			t_w.write(line + os.linesep)

		for line in val_list:
			v_w.write(line + os.linesep)


def multi_process(original_directory, corpus_train_directory, corpus_val_directory, map_path):
	for file in os.listdir(original_directory):
		t = multiprocessing.Process(target=conversion_fast_text, args=(
			os.path.join(original_directory, file), os.path.join(corpus_train_directory, file + '_train'),
			os.path.join(corpus_val_directory, file + '_val'),
			map_path))
		t.start()
