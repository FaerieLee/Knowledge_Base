#-*-coding:utf-8-*-
import random
import json
from data_process.data_import import importData
import os

file_path = "/home/ziqi/文档/solrData/solr-import-export-json/tmp/collection.json"
test_data_path = "/home/ziqi/文档/文件/test_data/solr_test_data"

with open(file_path, mode="r") as f, open(test_data_path, mode="w") as w:
	for line in f:
		if random.uniform(0, 1) > 0.999:
			w.write(json.dumps(importData.solr_dataset_adapter(json.loads(line))) + os.linesep)