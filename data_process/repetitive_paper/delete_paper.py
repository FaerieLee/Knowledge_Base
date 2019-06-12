# -*-coding:utf-8-*-

import sys

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import elasticsearch

"""
处理流程：
1.从文件(参数1)中读取删除文档的id
2.按照每批次的删除文档数量(参数2)以及id构建表达式,并执行批量删除操作
3.如果删除操作出现异常,将异常信息写入到文件(error_info)中
"""

if __name__ == "__main__":

	id_path = sys.argv[1]
	max_num = int(sys.argv[2])
	es_host = sys.argv[3]
	index_name = sys.argv[4]
	index_type = sys.argv[5]

	es = Elasticsearch(hosts=[es_host], timeout=5000)

	count = 0

	documents = []
	with open(id_path, encoding="utf-8", mode="r") as line_list, open("./error_info" , mode="r") as error_info:
		for line in line_list:  # 默认一行 为 一条数据
			document = {
				"_op_type": "delete",
				"_index": index_name,
				"_id": line.strip(),
				"_type": index_type,
			}
			documents.append(document)
			count += 1
			if count > max_num:
				try:
					bulk(es, documents)
				except elasticsearch.helpers.BulkIndexError as e:
					error_info.write(e)
				del documents[0:]
				count = 0
	if len(documents) > 0:
		try:
			bulk(es, documents)
		except elasticsearch.helpers.BulkIndexError as e:
			error_info.write(e)