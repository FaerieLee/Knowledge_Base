# -*-coding:utf-8-*-
from Knowledge_base.search.models.interface.search import Search, SearchCondition
from Knowledge_base.search.utils.utils import split_by_comma
import math
import copy


class AdvancedSearch(Search):

	def __init__(self, condition, config, agg, facet, query_dsl=Search.ADVANCED_SEARCH_TEMPLATE):
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


class AdvancedSearchCondition(SearchCondition):

	def __init__(self, title, author_name, author_org, venue,
				year, keywords, fos, lang, publisher, issn, doi, url, abstract):
		self.title = title
		self.author_name = author_name
		self.author_org = author_org
		self.venue = venue
		self.year = year
		self.keywords = keywords
		self.fos = fos
		self.lang = lang
		self.issn = issn
		self.publisher = publisher
		self.doi = doi
		self.url = url
		self.abstract = abstract

	def is_empty(self):
		return len(self.title) == 0 and len(self.author_name) == 0 and len(self.author_org) == 0 and len(self.venue) == 0 and len(self.year) == 0 and len(self.keywords) == 0 and len(self.fos) == 0 and len(self.lang) == 0 and len(self.issn) == 0 and len(self.publisher) == 0 and len(self.doi) == 0 and len(self.url) == 0 and len(self.abstract) == 0

	def build(self, query_dsl):

		must_clause: list = list()
		filter_clause: list = list()

		if self.title:
			must_clause.append({"match_phrase":
				{
					"title": self.title
				}
			})

		if self.author_name:
			must_clause.append({"match":
				{
					"authors.name.name_word": {
						"query": self.author_name,
						"operator": "and",
						"minimum_should_match": "75%"
					}
				}
			})

		if self.author_org:
			must_clause.append({"match_phrase":
				{
					"authors.org": self.author_org
				}
			})

		if self.abstract:
			must_clause.append({"match_phrase":
				{
					"abstract": self.abstract
				}
			})

		if self.venue:
			must_clause.append({"match_phrase":
				{
					"venue": self.venue
				}
			})

		if self.keywords:
			keyword_list = split_by_comma(self.keywords)
			filter_clause.append(
				{"terms_set":
					{"keywords":
						{
							"terms": keyword_list,
							"minimum_should_match_script":
								{
									"source": str(1)
									if 1 > math.ceil(len(keyword_list) * 0.6)
									else str(math.ceil(len(keyword_list) * 0.6))
								}
						}
					}
				}
			)

		if self.fos:
			fos_list = split_by_comma(self.fos)
			filter_clause.append({"terms_set":
				{"fos":
					{
						"terms": fos_list,
						"minimum_should_match_script":
							{
								"source": str(1)
								if 1 > math.ceil(len(fos_list) * 0.6)
								else str(math.ceil(len(fos_list) * 0.6))
							}
					}
				}
			}
			)

		if self.url:
			filter_clause.append({"term": {"url": self.url}})
		if self.publisher:
			filter_clause.append({"term": {"publisher": self.publisher}})
		if self.year:
			filter_clause.append({"term": {"year": self.year}})
		if self.lang:
			filter_clause.append({"term": {"lang": self.lang}})
		if self.issn:
			filter_clause.append({"term": {"issn": self.issn}})
		if self.doi:
			filter_clause.append({"term": {"doi": self.doi}})

		query_dsl['query']['bool']['must'] = must_clause
		query_dsl['query']['bool']['filter'] = filter_clause
