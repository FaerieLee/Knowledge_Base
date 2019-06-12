# -*-coding:utf-8-*-
from django.conf import settings

from Knowledge_base.search.models.interface.search import Search
import copy


class MatchAllFacetSearch(Search):

	def __init__(self, year, fos, publisher, author_name, query_dsl=Search.MATCH_ALL_FACET_SEARCH_TEMPLATE):
		self.year = year
		self.fos = fos
		self.publisher = publisher
		self.author_name = author_name
		self.query_dsl = copy.deepcopy(query_dsl)

	def is_empty(self):
		return len(self.year) == 0 and len(self.fos) == 0 and len(self.publisher) == 0 and len(self.author_name) == 0

	def build(self):

		filter_clause = self.query_dsl['query']['bool']['filter']

		if self.year:
			filter_clause.append({"terms": {
				"year": self.year
			}
			})

		if self.fos:
			fos_name_list = []
			for fos_id in self.fos:
				fos_name_list.append(settings.FOS_DICT[fos_id]['name'])

			filter_clause.append({"terms": {
				"fos": fos_name_list
			}
			})

		if self.author_name:
			filter_clause.append({"terms": {
				"authors.name": self.author_name
			}
			})

		if self.publisher:
			filter_clause.append({"terms": {
				"publisher": self.publisher
			}
			})

		return self.query_dsl