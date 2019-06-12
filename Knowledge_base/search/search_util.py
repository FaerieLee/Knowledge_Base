# -*-coding:utf-8-*-


#  获取用户的高级搜索的搜索项
def get_search_item(title, author_name, author_org, venue, year, keywords, fos, lang, publisher,
					issn, doi, url, abstract):

	search_item = dict()
	search_item["title"] = title
	search_item["author_name"] = author_name
	search_item["author_org"] = author_org
	search_item["venue"] = venue
	search_item["year"] = year
	search_item["keywords"] = keywords
	search_item["fos"] = fos
	search_item["lang"] = lang
	search_item["publisher"] = publisher
	search_item["issn"] = issn
	search_item["doi"] = doi
	search_item["url"] = url
	search_item["abstract"] = abstract
	search_item["title"] = title

	return search_item


def get_return_fields_body(fields_list):
	return {
		"_source": fields_list
	}


def get_search_id_body(paper_id):

	body = {
		"query": {
			"ids": {
				"values": paper_id
			}
		}
	}

	return body













