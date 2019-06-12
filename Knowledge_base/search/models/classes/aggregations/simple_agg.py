#-*-coding:utf-8-*-
from Knowledge_base.search.models.interface.search import SearchAggregation
from django.conf import settings


class SimpleAggregation(SearchAggregation):

	agg_body = {
		"aggs": {
			"year_agg": {
				"terms": {
					"field": "year",
					"size": 15,
					"order": {"_key": "desc"}
				}
			},
			"fos_agg": {
				"terms": {
					"field": "fos",
					"size": 19,
					"include": settings.LEVEL_0_FOS_LIST,
				}
			},
			"publisher_agg": {
				"terms": {
					"size": 10,
					"field": "publisher",
				}
			},
			"author_name_agg": {
				"terms": {
					"size": 10,
					"field": "authors.name",
				}
			}
		}
	}

	def build(self, query_dsl):
		query_dsl['aggs'] = self.agg_body['aggs']
		return
