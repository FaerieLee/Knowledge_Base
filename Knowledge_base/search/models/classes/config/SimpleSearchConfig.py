# -*-coding:utf-8-*-
from Knowledge_base.search.models.interface.search import SearchConfig, Search


class SimpleSearchConfig(SearchConfig):

	def __init__(self, page=1, size=10, source=Search.DEFAULT_RETURN_FIELDS, sort=""):
		self.from_ = (page-1) * size
		self.size = size
		self.source = source
		self.sort = sort

	def build(self, query_dsl):

		query_dsl['from'] = self.from_
		query_dsl['size'] = self.size
		query_dsl['indices_boost'] = [
			{"mag_aminer": 1.0},
			{"solr": 1.6}
		]
		query_dsl['track_total_hits'] = True
		if self.source:
			query_dsl['_source'] = self.source
		if self.sort:
			query_dsl['sort'] = self.sort
