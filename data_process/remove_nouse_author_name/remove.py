# -*-coding:utf-8-*-

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import re

es = Elasticsearch(hosts=["172.31.34.105:9200"], timeout=5000)
index_name = "aminer_mag"

pattern =  "([a-zA-Z0-9]|-|_)+(\.([a-zA-Z0-9]|-|_)+)*@([a-zA-Z0-9]|-|_)+(\.([a-zA-Z0-9]|-|_)+)+"

def main():
	fields = ['id', 'authors']

	body ={
		"size": 50,
		"_source": fields,
		"query":
			{
				"regexp": {
					"authors.name": ".*([a-z]|[A-Z]|[0-9]|_|-)+(\".\"[a-z]|[A-Z]|[0-9]|_|-)*\"@\"([a-z]|[A-Z]|[0-9]|_|-)+(\".\"([a-z]|[A-Z]|[0-9]|_|-)+)+.*"
				}
			}
	}

	result = es.search(index=index_name, body=body, scroll="1m")

	scroll_id = result['_scroll_id']
	doc_list = result['hits']['hits']

	while doc_list:
		updated_docs = []
		for doc in doc_list:
			tmp = doc['_source']
			tmp['id'] = doc['_id']
			if 'authors' in tmp:
				authors = []
				for ele in tmp['authors']:
					if 'name' in ele and re.search(pattern,ele['name']) != None:
						authors.append(ele)
				tmp['authors'] = authors
			updated_docs.append(tmp)

		update(updated_docs)

		doc_list = es.scroll(body={
			"scroll": "1m",
			"scroll_id": scroll_id
		})['hits']['hits']


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

	bulk(es, documents,index=index_name)


if __name__ == "__main__":
	main()

