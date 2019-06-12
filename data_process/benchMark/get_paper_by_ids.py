# -*-coding:utf-8-*-
from elasticsearch import Elasticsearch
import sys, os
import json


def translator(data):
	doc_list = []
	for ele in data['docs']:
		if 'found' in ele and ele['found']:
			doc_list.append(ele['_source'])
	return doc_list


if __name__ == "__main__":
	ids_path = sys.argv[1]  # 存放文档ｉｄ的路径
	documents_path = sys.argv[2]  # 获取到的文档存放的路径
	es_address = sys.argv[3]  # es地址
	index_name = sys.argv[4] # 索引名称
	doc_type = sys.argv[5] # 文档类型
	batch_num = 1000

	es = Elasticsearch(hosts=[es_address], timeout=5000)

	batch = []
	body = {
		'ids': batch
	}
	with open(ids_path, mode='r') as source, open(documents_path, mode='w') as dest:
		for doc_id in source:
			batch.append(doc_id.strip())
			if len(batch) > batch_num:
				body['ids'] = batch
				docs = es.mget(index=index_name, doc_type=doc_type, body=body)
				for doc in translator(docs):
					dest.write(json.dumps(doc) + os.linesep)
				del batch[0:]

		if len(batch) > 0:
			body['ids'] = batch
			docs = es.mget(index=index_name, doc_type=doc_type, body=body)
			for doc in translator(docs):
				dest.write(json.dumps(doc) + os.linesep)
