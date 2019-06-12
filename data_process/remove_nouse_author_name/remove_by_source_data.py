#-*-coding:utf-8-*-

# -*-coding:utf-8-*-
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import re
import json

es = Elasticsearch(hosts=["172.31.34.105:9200"], timeout=5000)
index_name = "aminer_mag"

pattern = "([a-zA-Z0-9]|-|_)+(\.([a-zA-Z0-9]|-|_)+)*@([a-zA-Z0-9]|-|_)+(\.([a-zA-Z0-9]|-|_)+)+"

def main():
	updated_docs = []
	with open("./docs_dd.txt", mode="r") as r:
		count =0
		for line in r:
			if len(line.strip()) > 0:
				print(line)
				doc = json.loads(line.strip())
				tmp = doc
				if 'authors' in tmp:
					authors = []
					for ele in tmp['authors']:
						if 'name' in ele and re.search(pattern,ele['name']) == None:
							authors.append(ele)
					tmp['authors'] = authors

				updated_docs.append(tmp)
				count += 1

			if count > 500:
				update(updated_docs)
				del updated_docs[0:]
	update(updated_docs)


def update(docs):

	documents = []
	for doc in docs:
		if 'authors' in doc:
			document = {
				"_op_type": "update",
				"_id": doc['id'],
				"_type": "pap",
				"doc": {
					"authors": doc['authors']
				}
			}
			documents.append(document)

	try:
		bulk(es, documents, index=index_name)
	except elasticsearch.helpers.BulkIndexError as e:
		print(e)


if __name__ == "__main__":
	main()