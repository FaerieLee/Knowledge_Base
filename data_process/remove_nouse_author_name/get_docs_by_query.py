#-*-coding:utf-8-*-

from elasticsearch import Elasticsearch
import json
import os

es = Elasticsearch(hosts=["172.31.34.105:9200"], timeout=5000)
index_name = ["aminer_mag"]

pattern =  "([a-zA-Z0-9]|-|_)+(\.([a-zA-Z0-9]|-|_)+)*@([a-zA-Z0-9]|-|_)+(\.([a-zA-Z0-9]|-|_)+)+"

def main():
	fields = ['id', 'authors']

	body ={
		"size": 200,
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

	with open("./docs_id.txt", mode="w") as w:
		while doc_list:
			for doc in doc_list:
				w.write(json.dumps(doc['_id']) + os.linesep)
			doc_list = es.scroll(body={
				"scroll": "1m",
				"scroll_id": scroll_id
			})['hits']['hits']


if __name__ == "__main__":
	main()

