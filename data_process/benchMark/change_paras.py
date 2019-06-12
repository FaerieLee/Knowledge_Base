# -*-coding:utf-8-*-
import json

source_file = "/home/ziqi/文档/文件/test_data/test.txt/track.json"
dest_file = "/home/ziqi/文档/文件/test_data/normal/track.json"

with open(source_file, mode="r") as source, open(dest_file, mode="w") as dest:
	data = json.load(source)

	for search in data['operations']:
		#search['body']['_source'] = ["id"]
		if 'aggs' in search['body']:
			search['body'].pop('aggs')

	json.dump(data, dest)