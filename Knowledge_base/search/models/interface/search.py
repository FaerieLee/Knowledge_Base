# -*-coding:utf-8-*-
import abc
from abc import ABCMeta


class SearchCondition:

	@abc.abstractmethod
	def build(self, query_dsl):
		pass


class SearchConfig:

	@abc.abstractmethod
	def build(self, query_dsl):
		return


class SearchAggregation:

	@abc.abstractmethod
	def build(self, query_dsl):
		return


class SearchFacet:

	@abc.abstractmethod
	def build(self, query_dsl):
		return


class Search:

	__metaclass = ABCMeta

	MATCH_ALL_TEMPLATE = {
		"query": {
			"match_all": {}
		}
	}

	GENERAL_SEARCH_TEMPLATE = {
		"query": {
			"bool": {
				"must": {
					"dis_max": {
						"queries": [
							{
								"match_phrase": {
									"title":
										{
											"query": None,
											"boost": 1.5
										}
								}
							},
							{
								"match": {
									"authors.name.name_word":
										{
											"query": None,
											"minimum_should_match": "75%"
										}
								}
							},
							{
								"match_phrase": {
									"authors.org":
										{
											"query": None
										}
								}
							}
						]
					}
				},
				"filter": []

			}
		}
	}

	ADVANCED_SEARCH_TEMPLATE = {
		"query": {
			"bool": {
				"must": [],
				"filter": []
				}
			}
		}

	MATCH_ALL_FACET_SEARCH_TEMPLATE = {
		"query": {
			"bool": {
				"filter": []
				}
			}
		}

	DEFAULT_RETURN_FIELDS = ["id", "title", "authors.name", "doi", "n_citation",
								"publisher", "year", "sub_abstract", "original"]

	condition: SearchCondition = None
	config: SearchConfig = None
	agg: SearchAggregation = None
	facet: SearchFacet = None

	query_dsl: dict = None

	@abc.abstractmethod
	def build(self):
		pass




