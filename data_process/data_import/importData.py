# -*-coding:utf-8-*-
import json
import sys
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

"""
读取文件数据,批量导入至es
"""

es = Elasticsearch(hosts=["114.115.129.20:9200"], timeout=5000)


def aminer_mag_adapter(fields):
	if 'abstract' in fields:
		fields['sub_abstract'] = fields['abstract'][0:150]
	return fields


def solr_dataset_adapter(fields):

	if 'subject' in fields:
		fields['fos'] = fields['subject']
		fields.pop('subject')
	if 'preview' in fields:
		fields['abstract'] = fields['preview']
		fields['sub_abstract'] = fields['preview'][0:170]
		fields.pop('preview')
	if 'pid' in fields:
		fields['id'] = fields['pid']
		fields.pop('pid')
	if 'journal' in fields:
		fields['publisher'] = fields['journal']
		fields.pop('journal')
	if 'kwd' in fields:
		fields['keywords'] = fields['kwd']
		fields.pop('kwd')
	if "ref" in fields:
		fields['references'] = fields['ref']
		fields.pop('ref')
	if 'author' in fields:
		author_list = []
		i = 0

		if 'author_aff' in fields and len(fields['author']) == len(fields['author_aff']):
			for author in fields['author']:
				ele = dict()
				ele['name'] = author
				ele['org'] = fields['author_aff'][i]
				author_list.append(ele)
			if 'author_aff' in fields and len(fields['author']) != len(fields['author_aff']):
				i += 1
		else:
			for author in fields['author']:
				ele = dict()
				ele['name'] = author
				author_list.append(ele)
		fields['authors'] = author_list
		fields.pop('author')
	if 'author_aff' in fields:
		fields.pop('author_aff')

	return fields


def insert(path):  # 每次提交到 elasticsearch 的document个数

		global max_num, index_name
		documents = []
		count = 0
		with open(path, encoding="utf-8", mode="r") as line_list:
				for line in line_list:  # 默认一行 为 一条数据
					try:
						fields = json.loads(line)
						document = {
							"_index": index_name,
							"_id": fields['id'],
							"_source": aminer_mag_adapter(fields)
						}
						documents.append(document)
						count += 1
						if count > max_num:
							bulk(es, documents, chunk_size=max_num+5, stats_only= True)
							del documents[0:]
							count = 0
					except json.decoder.JSONDecodeError as e:
						# 可能会遇到解析json数据错误,对于此类数据,忽略而过
						print(path, e)
						continue
		if len(documents) > 0:
			bulk(es, documents, chunk_size=max_num+5,stats_only= True)
			del documents[0:]


if __name__ == "__main__":

	# sys.argv传入的参数为字符串类型，如果想做一些条件判断的话需要转成你所需要的数据类型

	file_url = sys.argv[1]  # 存放文件的文件夹位置
	max_num = int(sys.argv[2])  # 每批提交的文档数量,7000
	index_name = sys.argv[3]  # index名字

	init_time = time.time()
	print("current_time : ", init_time)

	insert(file_url)

	print("导入数据所需时间：", time.time() - init_time)
