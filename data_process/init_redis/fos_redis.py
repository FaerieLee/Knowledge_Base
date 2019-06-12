#- *-coding:utf-8-*-

import os,copy
import json

from elasticsearch import Elasticsearch

from Knowledge_base.search.utils.fos_init import init_fos

"""
从一级学科出发，递归获取每一学科下子学科中文档数量排名前十的学科信息，直至递归结束。此部分信息需要缓存到redis中。
"""

LEVEL_0_FOS_URL = 'data/level_0_fos'
FOS_DIR = 'data/fos'
BASE_DIR = '/home/ziqi/PycharmProjects/Knowledge_Base'

FOS_AGG_TEMPLATE = {
		"size":0,
		"aggs": {
			"fos_agg": {
				"terms": {
					"field": "fos",
					"size": 10,
					"include": [],
				}
			}
		}
	}


def get_fos_init():

    level_0_fos_url = os.path.join(BASE_DIR, LEVEL_0_FOS_URL)
    fos_dir = os.path.join(BASE_DIR, FOS_DIR)

    # root_fos, fos_dict: format:{ "fos_id":{“name”:name1, "child":[]},....}
    level_0_fos, fos_dict = init_fos(level_0_fos_url, fos_dir)

    level_0_fos_list = []
    level_0_fos_mapper = {} # name -> id
    for fos in level_0_fos:
        level_0_fos_list.append(level_0_fos[fos]['name'])
        level_0_fos_mapper[level_0_fos[fos]['name']] = fos

    return fos_dict, level_0_fos_list, level_0_fos_mapper


# 初始化学科层级
FOS_DICT, LEVEL_FOS_LIST, LEVEL_0_FOS_MAPPER = get_fos_init()

NAME_ID_MAPPER = dict()

for key, value in FOS_DICT.items():
    NAME_ID_MAPPER[value['name'].lower()] = key

for key, value in LEVEL_0_FOS_MAPPER.items():
    NAME_ID_MAPPER[key] = value

es = Elasticsearch(hosts="114.115.129.20:9200", timeout=500000)

id_set= set()

url = "./result.txt"
with open(url, mode="w") as writer:
    while LEVEL_FOS_LIST:

        agg_body = copy.deepcopy(FOS_AGG_TEMPLATE)
        sub_fos_name_list = []  # format:[name1,name2....]
        sub_fos_list = []
        random_fos_id = NAME_ID_MAPPER[LEVEL_FOS_LIST.pop()]

        if random_fos_id in id_set:
            pass
        else:
            id_set.add(random_fos_id)
            sub_fos_list = FOS_DICT[random_fos_id]['child']

        if sub_fos_list:

            for fos_tuple in sub_fos_list:
                sub_fos_name_list.append(fos_tuple[1])

            agg_body['aggs']['fos_agg']['terms']['include'] = sub_fos_name_list

            result = es.search(index="mag_aminer", doc_type="_doc", body=agg_body)

            fos_agg_info = []
            for agg_dict in result['aggregations']['fos_agg']['buckets']:
                writer.write(json.dumps({
                    "id": NAME_ID_MAPPER[agg_dict['key']],
                    "name": agg_dict['key'],
                    "count": agg_dict['doc_count']}) + os.linesep)
                LEVEL_FOS_LIST.append(agg_dict['key'])





