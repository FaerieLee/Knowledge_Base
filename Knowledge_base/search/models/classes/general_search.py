# -*-coding:utf-8-*-
from Knowledge_base.search.models.interface.search import Search, SearchCondition
import copy


class GeneralSearch(Search):

	def __init__(self, condition, config, agg, facet, query_dsl=Search.GENERAL_SEARCH_TEMPLATE):
		self.condition = condition
		self.config = config
		self.agg = agg
		self.facet = facet
		self.query_dsl = copy.deepcopy(query_dsl)

	def build(self):
		if self.condition:
			self.condition.build(self.query_dsl)
		if self.config:
			self.config.build(self.query_dsl)
		if self.agg:
			self.agg.build(self.query_dsl)
		if self.facet:
			self.facet.build(self.query_dsl)
		return self.query_dsl


class GeneralSearchCondition(SearchCondition):

	def __init__(self, content):
		self.content = content

	def is_empty(self):
		return len(str(self.content).strip()) == 0

	def build(self, query_dsl):

		dis_max_clause = query_dsl['query']['bool']['must']['dis_max']['queries']

		dis_max_clause[0]['match_phrase']['title']['query'] = self.content
		dis_max_clause[1]['match']['authors.name.name_word']['query'] = self.content
		dis_max_clause[2]['match_phrase']['authors.org']['query'] = self.content
