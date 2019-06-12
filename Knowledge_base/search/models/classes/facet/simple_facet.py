# -*-coding:utf-8-*-
from Knowledge_base.search.models.interface.search import SearchFacet
from django.conf import settings


class SimpleSearchFacet(SearchFacet):
	def __init__(self, year, fos, publisher, author_name):
		self.year = year
		self.fos = fos
		self.publisher = publisher
		self.author_name = author_name

	def is_empty(self):
		return len(self.year) == 0 and len(self.fos) == 0 and len(self.publisher) == 0 and len(self.author_name) == 0

	def build(self, query_dsl):

		filter_clause = query_dsl['query']['bool']['filter']

		if self.year:
			filter_clause.append({"terms": {
					"year": self.year
				}
			})

		if self.fos:
			fos_name_list = []
			for fos_id in self.fos:
				fos_name_list.append(settings.FOS_DICT[fos_id]['name'])

			print(fos_name_list)
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