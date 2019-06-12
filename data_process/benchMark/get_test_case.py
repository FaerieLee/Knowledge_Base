# -*-coding:utf-8-*-
import json
import random

from Knowledge_base.search import search_util


def main():
	data_paths = ["/home/ziqi/文档/文件/test_data/testX/aminer_test_data",
				"/home/ziqi/文档/文件/test_data/testX/mag_test_data",
				"/home/ziqi/文档/文件/test_data/testX/solr_test_data"]
	dest_path = "/home/ziqi/文档/文件/test_data/test.txt/track.json"
	with open("./rally_base.json", mode="r") as base:
		cases = json.load(base)

	count = 0
	for path in data_paths:
		with open(path, mode='r') as docs:
			for doc in docs:
				try:
					fields = json.loads(doc)
					case = dict()
					case['name'] = str(count)
					case['body'] = get_search_body(fields)
					case['operation-type'] = 'search'
					case['pages'] = 1
					case['cache'] = True
					case['results-per-page'] = 10
					cases['operations'].append(case)
					count += 1
				except json.decoder.JSONDecodeError as e:
					print(e)
					continue
	with open(dest_path, mode="w") as f:
		json.dump(cases, f)


def get_search_body(doc):
	if random.randint(1, 10) < 11:
		return get_advance_body(doc)
	else:
		return get_general_body(doc)


def get_advance_body(doc):

	title = get_attr_whole(doc, 'title')[0:80]
	lang =  get_attr_whole(doc, 'lang')
	publisher = get_attr_whole(doc, 'publisher')[0:80]
	issn = get_attr_whole(doc, 'issn')
	doi = get_attr_whole(doc, 'doi')

	year =  get_attr_whole(doc, 'year')
	venue = get_attr_whole(doc, 'venue')[0:80]

	author_name = get_attr_part(doc, "author_name")[0:30]
	author_org = get_attr_part(doc, "author_org")[0:30]
	keywords = get_attr_part(doc, "keywords")
	fos = get_attr_part(doc, "fos")
	url = get_attr_part(doc, 'url')

	abstract = ""
	#if "abstract" in doc:
	#	if random.randint(0, 1) == 0:
	#		abstract = doc["abstract"][0:128]

	query_body = search_util.get_query_advanced_body(title, author_name, author_org, venue,
													 str(year), keywords, fos, lang, publisher, issn, doi, url, abstract)

	size_body, fields_body, sort_body, agg_body = except_query_body()

	search_body = search_util.get_search_body(query_body, size_body, fields_body, sort_body, agg_body)

	return search_body


def get_general_body(doc):

	random_num = random.randint(0, 2)
	if random_num == 0:
		query_body = search_util.get_search_general_body(get_attr_whole(doc, 'title'))
	elif random_num == 1:
		query_body = search_util.get_search_general_body(get_attr_part(doc, "author_name"))
	else:
		query_body = search_util.get_search_general_body(get_attr_part(doc, "author_org"))

	size_body, fields_body, sort_body, agg_body = except_query_body()

	search_body = search_util.get_search_body(query_body, size_body, fields_body, sort_body, agg_body)

	return search_body


def get_attr_whole(doc, field_name):
	if field_name in doc:
		return "" if random.randint(0,1) == 0 else doc[field_name]
	else:
		return ""


def get_attr_part(doc, field_name):
	result = ""
	if field_name == 'author_name':
		if 'authors' in doc:
			for author in doc["authors"]:
				if 'name' in author:
					result += (("" if random.randint(0,1) else author['name']) + "," )
	elif field_name == 'author_org':
		if 'authors' in doc:
			for author in doc["authors"]:
				if 'org' in author:
					result += (("" if random.randint(0, 1) else author['org']) + ",")
	elif field_name == 'url':
		if 'url' in doc:
			result += doc['url'][random.randint(1, len(doc['url'])) -1 ]
	else:
		if field_name in doc:
			for ele in doc[field_name]:
				result += ("" if random.randint(0, 1) else ele + ",")

	return result


def except_query_body():

	size_body = search_util.get_size_body(from_=(1 - 1) * 10, size=10)

	# 将“前端传来的字段名称”转化为“后端的字段名称”
	sort_num = random.randint(0, 2)
	#if sort_num == 0:
	#	sort_body = search_util.get_sort_body("Year", "desc")
	#elif sort_num == 1:
	#	sort_body = search_util.get_sort_body("Citation", "desc")
	#else:
	sort_body = dict()

	fields = ["id", "title", "authors.name", "doi", "n_citation", "publisher", "year", "sub_abstract", "original"]
	root_fos_list = ['political science', 'economics', 'history', 'engineering', 'sociology', 'biology', 'mathematics',
					'medicine', 'geography', 'chemistry', 'art', 'computer science', 'materials science',
					'psychology', 'environmental science', 'business', 'geology', 'physics', 'philosophy']

	fields_body = search_util.get_return_fields_body(fields)

	agg_body = []
		#search_util.get_aggregation_body(root_fos_list)

	return size_body, fields_body, sort_body, agg_body


if __name__ == "__main__":
	main()