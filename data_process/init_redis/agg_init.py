# -*-coding:utf-8-*-
from elasticsearch import Elasticsearch
import json
import os


"""
获取es数据的统计信息，此部分信息需要缓存到redis中。
"""
es = Elasticsearch(hosts="172.31.34.104:9200", timeout=500000)

agg_body = {
  "track_total_hits": True,
  "size": 0,
  "aggs": {
		"year_agg": {
				"terms": {
				  "size":25,
					"field": "year",
					"order": {"_key": "desc"}
				}
			},
			"fos_agg": {
				"terms": {
					"size": 19,
					"field": "fos",
					"include": ["physics","biology","materials science","chemistry","environmental science",
								"mathematics","computer science","psychology","sociology","geology",
								"political science","geography","medicine","history","art","philosophy",
								"engineering","business","economics"]
				}
			},
			"author_name_agg": {
				"terms": {
					"size": 30,
					"field": "authors.name"
				}
			},
			"publisher_agg": {
				"terms":{
					"size": 12,
					"field":"publisher"
			}
		}
	}
}

result = es.search(index="mag_aminer", body=agg_body)

print(result['hits'])

for key in result['aggregations']:
	with open(key, mode="w") as writer:
		for elements in result['aggregations'][key]['buckets']:
			writer.write(json.dumps(elements) + os.linesep)
