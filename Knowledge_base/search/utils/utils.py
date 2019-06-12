# -*-coding:utf-8-*-
from django.conf import settings
import re
import json
import xml.etree.cElementTree as ET
import copy


def conversion_including_agg(result):

	"""

	解析Elasticsearch返回结果, 其中包含相关指标的聚合信息
	:param result: Elasticsearch查询返回的字典类型结果
	:return: 文章信息列表, 页数, 时间 出版社 学科 作者名称的聚合结果

	"""

	paper_list = []

	for paper in result['hits']['hits']:
		paper['_source']['id'] = paper['_id']
		paper_list.append(paper['_source'])

	papers_num = result['hits']['total']['value']

	aggs = result['aggregations']
	year_agg_info = aggs['year_agg']['buckets']
	publisher_agg_info = aggs['publisher_agg']['buckets']
	author_name_agg_info = aggs['author_name_agg']['buckets']

	fos_agg_info = []
	for agg_dict in aggs['fos_agg']['buckets']:
		fos_agg_info.append({
			"id": settings.LEVEL_0_FOS_MAPPER[agg_dict['key']],
			"name": agg_dict['key'],
			"count": agg_dict['doc_count'],
		})

	return paper_list, papers_num, year_agg_info, publisher_agg_info, fos_agg_info, author_name_agg_info


def conversion_fos(fos_agg):
	fos_agg_info = []
	for agg_dict in fos_agg:
		fos_agg_info.append({
			"id": settings.LEVEL_0_FOS_MAPPER[agg_dict['key']],
			"name": agg_dict['key'],
			"count": agg_dict['doc_count'],
		})
	return fos_agg_info


def conversion_match_all_search(result):
	paper_list = []

	for paper in result['hits']['hits']:
		paper['_source']['id'] = paper['_id']
		paper_list.append(paper['_source'])

	return paper_list


def conversion_not_including_agg(result):

	"""

	解析Elasticsearch返回结果, 只包含文章信息列表
	:param result: Elasticsearch查询返回的字典类型结果
	:return: 文章信息列表, 文章数量

	"""

	paper_list = []

	for paper in result['hits']['hits']:
		paper['_source']['id'] = paper['_id']
		paper_list.append(paper['_source'])

	paper_num = result['hits']['total']['value']
	return paper_list, paper_num


def conversion_sort_field(sort_name):

	"""

	字段名称的转化：由于前端与Elasticsearch排序字段名称的不一致，所以需要转换操作
	:param sort_name: 前端的排序字段名称
	:return: Elasticsearch对应排序字段名称

	"""

	if sort_name == "Year":
		return "year"
	elif sort_name == "Citation":
		return "n_citation"
	else:
		return ""


def split_by_comma(sentence=''):
	result = []
	if sentence:
		for token in re.split(r'[,，]', sentence):
			if len(token.strip()) > 0:
				result.append(token.strip())
	return result


def conversion_sub_fos_agg(result, name_id_mapper):
	fos_agg_info = []
	for agg_dict in result['aggregations']['fos_agg']['buckets']:
		fos_agg_info.append({
			"id": name_id_mapper[agg_dict['key']],
			"name": agg_dict['key'],
			"count": agg_dict['doc_count'],
	})

	return json.dumps(fos_agg_info)


def conversion_paper_detail(result, index, es):

	paper_detail = result['_source']
	paper_detail['id'] = result['_id']

	if 'authors' in paper_detail:
		authors_list = paper_detail['authors']
		name, org = get_author_name_org_format(authors_list)
		del paper_detail['authors']
		paper_detail['name'] = name
		paper_detail['org'] = org

	if 'references' in paper_detail:

		if 'solr' in index:
			pass
		else:
			references = []
			tmp = dict()

			doc_references = get_reference_info_by_ids(settings.ELASTIC['INDEX'], paper_detail['references'], es)
			for reference in doc_references['docs']:

				print(reference)
				if reference['found']:
					tmp['id'] = reference['_id']
					tmp['title'] = reference['_source']['title']
					references.append(copy.deepcopy(tmp))
					tmp.clear()
			paper_detail['references'] = references

	return paper_detail


def conversion_paper_download(result, index, es):

	paper_download = result['_source']
	paper_download['id'] = result['_id']

	if 'sub_abstract' in paper_download:
		del paper_download['sub_abstract']

	if 'references' in paper_download:

		if 'solr' in index:
			pass
		else:
			references = []
			tmp = dict()

			doc_references = get_reference_info_by_ids(settings.ELASTIC['INDEX'], paper_download['references'], es)
			for reference in doc_references['docs']:
				if reference['found']:
					tmp['id'] = reference['_id']
					tmp['tile'] = reference['_source']['title']
					references.append(tmp)
			paper_download['references'] = references

	return paper_download


def conversion_dict_to_xml(paper):
	root = ET.Element('article')
	article_id = ET.SubElement(root, 'article-id')
	article_id.text = paper['id']
	if 'title' in paper:
		article_title = ET.SubElement(root, 'article-title')
		article_title.text = paper['title']
	if 'authors' in paper:
		authors = ET.SubElement(root, 'authors')
		for author_info in paper['authors']:
			author = ET.SubElement(authors, 'authors')
			if 'name' in author_info:
				name = ET.SubElement(author, 'name')
				name.text = author_info['name']
			if 'org' in author_info:
				org = ET.SubElement(author, 'org')
				org.text = str(author_info['org'])
	if 'doc_type' in paper:
		doc_type = ET.SubElement(root, 'doc_type')
		doc_type.text = paper['doc_type']
	if 'doi' in paper:
		doi = ET.SubElement(root, 'doi')
		doi.text = paper['doi']
	if 'fos' in paper:
		fos = ET.SubElement(root, 'fos')
		fos.text = ','.join(paper['fos'])
	if 'isbn' in paper:
		isbn = ET.SubElement(root, 'isbn')
		isbn.text = str(paper['isbn'])
	if 'issn' in paper:
		issn = ET.SubElement(root, 'issn')
		issn.text = str(paper['issn'])
	if 'issue' in paper:
		issue = ET.SubElement(root, 'issue')
		issue.text = str(paper['issue'])
	if 'keywords' in paper:
		keywords = ET.SubElement(root, 'keywords')
		keywords.text = ','.join(paper['keywords'])
	if 'lang' in paper:
		lang = ET.SubElement(root, 'lang')
		lang.text = paper['lang']
	if 'page_start' in paper:
		page_start = ET.SubElement(root, 'page_start')
		page_start.text = str(paper['page_start'])
	if 'page_end' in paper:
		page_end = ET.SubElement(root, 'page_end')
		page_end.text = str(paper['page_end'])
	if 'n_citation' in paper:
		n_citation = ET.SubElement(root, 'n_citation')
		n_citation.text = str(paper['n_citation'])
	if 'year' in paper:
		year = ET.SubElement(root, 'year')
		year.text = str(paper['year'])
	if 'volume' in paper:
		volume = ET.SubElement(root, 'volume')
		volume.text = str(paper['volume'])
	if 'original' in paper:
		original = ET.SubElement(root, 'original')
		original.text = paper['original']
	if 'abstract' in paper:
		abstract = ET.SubElement(root, 'abstract')
		abstract.text = paper['abstract']
	if 'url' in paper:
		urls = ET.SubElement(root, 'urls')
		for url in paper['url']:
			url_tag = ET.SubElement(urls, 'url')
			url_tag.text = url
	if 'pdf' in paper:
		pdfs = ET.SubElement(root, 'pdfs')
		for pdf in paper['pdf']:
			pdf_tag = ET.SubElement(pdfs, 'pdf')
			pdf_tag.text = pdf
	if 'references' in paper:
		references = ET.SubElement(root, 'references')
		for reference in paper['references']:
			ref = ET.SubElement(references, 'ref')
			if type(reference) == str:
				title = ET.SubElement(ref, 'title')
				title.text = reference
			else:
				if 'id' in reference:
					name = ET.SubElement(ref, 'id')
					name.text = reference['id']
				if 'title' in reference:
					title = ET.SubElement(ref, 'title')
					title.text = reference['title']
	return root


def get_index_by_id(paper_id):

	if len(paper_id) == 19:
		return 'solr'
	else:
		return 'mag_aminer'


def get_author_name_org_format(authors_list):
	"""
	格式化作者名字cd，机构
	将[{'name':"xx",'org':'ss'},...] 转化为字符串表示, 'name': 1.xx 2.xx ... 'org': 1.ss 2.dd..
	:param authors_list:
	:return:
	"""
	name_index = 1
	org_index = 1
	name = ''
	org = ''
	for author in authors_list:
		if 'name' in author:
			name = name + str(name_index) + '. ' + author['name'] + ' '
			name_index += 1
		if 'org' in author:
			org = org + str(org_index) + '. ' + author['org'] + ' '
			org_index += 1
	return name, org


def get_reference_info_by_ids(index_name, ids, es):

	body = {
		'ids': ids
	}

	reference_info = ['id', 'title']

	try:
		result = es.mget(index=index_name, body=body, _source=reference_info)
	except:
		print(result)
	print(result)
	return result

