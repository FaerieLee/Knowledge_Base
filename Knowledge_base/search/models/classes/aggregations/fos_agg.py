# -*-coding:utf-8-*-


from Knowledge_base.search.models.interface.search import SearchAggregation
from django.conf import settings
import copy


class FosAggregation(SearchAggregation):

	FOS_AGG_TEMPLATE = {
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

	def build(self, query_dsl):
		query_dsl['aggs'] = self.agg_body['aggs']
		return

	def __init__(self, fos_id):
		self.fos_id = fos_id
		self.agg_body = copy.deepcopy(FosAggregation.FOS_AGG_TEMPLATE)
		sub_fos_name_list = []  # format:[name1,name2....]
		sub_fos_name_id_mapper = dict()
		if self.fos_id:
			sub_fos_list = settings.FOS_DICT[self.fos_id]['child']
			if sub_fos_list:
				for fos_tuple in sub_fos_list:
					sub_fos_name_list.append(fos_tuple[1])
					sub_fos_name_id_mapper[fos_tuple[1]] = fos_tuple[0]

		self.name_id_mapper = sub_fos_name_id_mapper

		self.agg_body['aggs']['fos_agg']['terms']['include'] = sub_fos_name_list
