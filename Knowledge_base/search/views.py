# -*-coding:utf-8-*-
import elasticsearch
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings
from elasticsearch import Elasticsearch
from django.views.decorators.csrf import csrf_exempt

from Knowledge_base.search.models.classes.advanced_search import AdvancedSearchCondition, AdvancedSearch
from Knowledge_base.search.models.classes.aggregations.fos_agg import FosAggregation
from Knowledge_base.search.models.classes.aggregations.simple_agg import SimpleAggregation
from Knowledge_base.search.models.classes.config.SimpleSearchConfig import SimpleSearchConfig
from Knowledge_base.search.models.classes.facet.simple_facet import SimpleSearchFacet
from Knowledge_base.search.models.classes.general_search import GeneralSearchCondition, \
    GeneralSearch
from Knowledge_base.search.models.classes.match_all_facet_search import MatchAllFacetSearch
from Knowledge_base.search.models.interface.search import Search
from Knowledge_base.search.utils.utils import conversion_including_agg, conversion_not_including_agg, \
    conversion_sort_field, split_by_comma, conversion_sub_fos_agg, get_index_by_id, conversion_paper_detail, \
    conversion_paper_download, conversion_dict_to_xml, conversion_match_all_search
from Knowledge_base.search import search_util
import json
import math
from Knowledge_base import settings
import xml.etree.cElementTree as ET
from django.core.cache import cache


es = Elasticsearch(hosts=settings.ELASTIC['ADDRESS'], timeout=5000)


def index(request):
    return render(request, 'paper/index.html')


def download(request):

    paper_id = request.GET.get("paper_id", default="")
    file_format = request.GET.get("format", default="json")

    index_name = get_index_by_id(paper_id)
    result = es.get(index=index_name, doc_type=settings.ELASTIC['DOC_TYPE'], id=paper_id, routing=paper_id)
    paper_download = conversion_paper_download(result, index_name, es)

    if file_format == 'json':
        response = JsonResponse(paper_download)
        response["Content-Disposition"] = "attachment;filename={}".format(str(paper_download['id']) + '.json')
        return response

    elif file_format == 'xml':
        root = conversion_dict_to_xml(paper_download)
        tree = ET.ElementTree(root)
        file_url = paper_download['id'] + '.xml'
        tree.write(file_url, xml_declaration=True, encoding='utf-8')
        response = FileResponse(open(file_url, mode="rb"))
        response['Content-Type'] = 'application/xml'
        response['Content-Disposition'] = 'attachment;filename={}'.format(str(paper_download['id'] + '.xml'))
        return response
    else:
        pass


@csrf_exempt
def get_paper_by_id(request):

    paper_id = request.GET.get("paper_id", default="")

    index_name = get_index_by_id(paper_id)
    try:
        result = es.get(index=index_name, id=paper_id, routing=paper_id,
                        _source=settings.PAPER_DETAIL_FIELDS)
        paper_detail = conversion_paper_detail(result, index_name, es)

        return render(request, "paper/paper_detail.html", {"paper": paper_detail, "data_set": index_name})
    except elasticsearch.exceptions.NotFoundError:
        return HttpResponseNotFound("None")


@csrf_exempt
def search_general(request):

    info = request.POST.get("search_content", default="")

    page = int(request.POST.get("page", default=1))
    sort = conversion_sort_field(request.POST.get("sort", default="").strip())

    is_agg = request.POST.get("aggregation", default=False)

    facet_year = split_by_comma(request.POST.get("year_facet", default=""))
    facet_fos_id = split_by_comma(request.POST.get("fos_facet", default=""))
    facet_author = split_by_comma(request.POST.get("author_facet", default=""))
    facet_publisher = split_by_comma(request.POST.get("publisher_facet", default=""))

    condition = GeneralSearchCondition(content=info)
    config = SimpleSearchConfig(page=page, sort=sort)

    if is_agg:
        agg = SimpleAggregation()
    else:
        agg = None

    facet = SimpleSearchFacet(facet_year, facet_fos_id, facet_publisher, facet_author)

    if condition.is_empty():
        if facet.is_empty():
            search_body = Search.MATCH_ALL_TEMPLATE
        else:
            search_body = MatchAllFacetSearch(facet_year, facet_fos_id, facet_publisher, facet_author).build()
        size = 10
        search_body['from'] = (page - 1) * size
        search_body['size'] = size
        search_body['_source'] = Search.DEFAULT_RETURN_FIELDS
        if len(sort) > 0:
            search_body['sort'] = {
                sort:{"order" : "desc"}
            }

    else:
        search_body = GeneralSearch(condition=condition, config=config, agg=agg, facet=facet).build()

    result = es.search(index=settings.ELASTIC['INDEX'], body=search_body)

    if is_agg:

        if condition.is_empty() and facet.is_empty():
                paper_list = conversion_match_all_search(result)
                paper_num = settings.PAPER_NUM
                year_agg_info = settings.YEAR_AGG_INFO
                publisher_agg_info = settings.PUBLISHER_AGG_INFO
                fos_agg_info = settings.FOS_AGG_INFO
                author_name_agg_info = settings.AUTHOR_NAME_AGG_INFO
        else:
            paper_list, paper_num, year_agg_info, publisher_agg_info, fos_agg_info, author_name_agg_info = \
                conversion_including_agg(result)

        # 生成一个页码的列表，大于9页只显示9页，否则全部显示
        return render(request, 'paper/home.html', {"paper_list": paper_list,
                                                   "page_num_list": range(math.ceil(paper_num/10)
                                                                          if math.ceil(paper_num/10) < 10 else 9),
                                                   "page_num": math.ceil(paper_num/10),
                                                   "search_content": info,
                                                   "search_type": "general",
                                                   "result_num": paper_num,
                                                   "years": year_agg_info, "foses": fos_agg_info,
                                                   "publishers": publisher_agg_info, "authors": author_name_agg_info
                                                   })
    else:

        paper_list, papers_num = conversion_not_including_agg(result)
        if condition.is_empty():
            num = 0
            for year in facet_year:
                for each_dict in settings.YEAR_AGG_INFO:
                    if each_dict['key'] == year:
                        num += each_dict['doc_count']
            for author in facet_author:
                for each_dict in settings.AUTHOR_NAME_AGG_INFO:
                    if each_dict['key'] == author:
                        num += each_dict['doc_count']
            for publisher in facet_publisher:
                for each_dict in settings.PUBLISHER_AGG_INFO:
                    if each_dict['key'] == publisher:
                        num += each_dict['doc_count']

            for fos_id in facet_fos_id:
                count = cache.get(fos_id)
                if isinstance(count, int):
                    num += count

            if num == 0:
                papers_num = settings.PAPER_NUM
            else:
                papers_num = num
        return HttpResponse(json.dumps({"data": paper_list,
                                        "page_num": math.ceil(papers_num/10),
                                        "result_num": papers_num}))


@csrf_exempt
def search_advanced(request):

    title = request.POST.get("title", default="").strip()
    author_name = request.POST.get("author_name", default="").strip()
    author_org = request.POST.get("author_org", default="").strip()
    venue = request.POST.get("venue", default="").strip()
    year = request.POST.get("year", default="").strip()
    keywords = request.POST.get("keywords", default="").strip()
    fos = request.POST.get("fos", default="").strip()
    lang = request.POST.get("lang", default="").strip()
    publisher = request.POST.get("publisher", default="").strip()
    issn = request.POST.get("issn", default="").strip()
    doi = request.POST.get("doi", default="").strip()
    url = request.POST.get("url", default="").strip()
    abstract = request.POST.get("abstract", default="").strip()

    page = int(request.POST.get("page", default=1))
    sort = conversion_sort_field(request.POST.get("sort", default="").strip())

    is_agg = request.POST.get("aggregation", default=False)
    facet_year = split_by_comma(request.POST.get("year_facet", default=""))
    facet_author = split_by_comma(request.POST.get("author_facet", default=""))
    facet_publisher = split_by_comma(request.POST.get("publisher_facet", default=""))
    facet_fos_id = split_by_comma(request.POST.get("fos_facet", default=""))

    condition = AdvancedSearchCondition(title=title, author_name=author_name, author_org=author_org, venue=venue,
                                        year=year, keywords=keywords, fos=fos, lang=lang, publisher=publisher,
                                        issn=issn, doi=doi, url=url, abstract=abstract)

    config = SimpleSearchConfig(page=page, sort=sort)

    if is_agg:
        agg = SimpleAggregation()
    else:
        agg = None

    facet = SimpleSearchFacet(facet_year, facet_fos_id, facet_publisher, facet_author)

    if condition.is_empty():
        if facet.is_empty():
            search_body = Search.MATCH_ALL_TEMPLATE
        else:
            search_body = MatchAllFacetSearch(facet_year, facet_fos_id, facet_publisher, facet_author).build()
        size = 10
        search_body['from'] = (page - 1) * size
        search_body['size'] = size
        search_body['_source'] = Search.DEFAULT_RETURN_FIELDS
        if len(sort) > 0:
            search_body['sort'] = {
                sort: {"order": "desc"}
            }
    else:
        search_body = AdvancedSearch(condition=condition, config=config, agg=agg, facet=facet).build()

    result = es.search(index=settings.ELASTIC['INDEX'],body=search_body)

    if is_agg:

        if condition.is_empty() and facet.is_empty():
            paper_list = conversion_match_all_search(result)
            paper_num = settings.PAPER_NUM
            year_agg_info = settings.YEAR_AGG_INFO
            publisher_agg_info = settings.PUBLISHER_AGG_INFO
            fos_agg_info = settings.FOS_AGG_INFO
            author_name_agg_info = settings.AUTHOR_NAME_AGG_INFO
        else:
            paper_list, paper_num, year_agg_info, publisher_agg_info, fos_agg_info, author_name_agg_info = \
                conversion_including_agg(result)

        items = search_util.get_search_item(title, author_name, author_org, venue, year, keywords, fos, lang, publisher,
                                            issn, doi, url, abstract)  # 高级搜索项的json数据表示，用于主页显示

        return render(request, 'paper/home.html', {"paper_list": paper_list,
                                                   "page_num_list": range(math.ceil(paper_num/10)
                                                                          if math.ceil(paper_num/10) < 10 else 9),
                                                   "page_num": math.ceil(paper_num/10),
                                                   "items": items,
                                                   "search_type": "advanced",
                                                   "result_num": paper_num,
                                                   "years": year_agg_info, "foses": fos_agg_info,
                                                   "publishers": publisher_agg_info, "authors": author_name_agg_info
                                                   })
    else:
        paper_list, papers_num = conversion_not_including_agg(result)
        if condition.is_empty():
            num = 0
            for year in facet_year:
                for each_dict in settings.YEAR_AGG_INFO:
                    if each_dict['key'] == year:
                        num += each_dict['doc_count']
            for author in facet_author:
                for each_dict in settings.AUTHOR_NAME_AGG_INFO:
                    if each_dict['key'] == author:
                        num += each_dict['doc_count']
            for publisher in facet_publisher:
                for each_dict in settings.PUBLISHER_AGG_INFO:
                    if each_dict['key'] == publisher:
                        num += each_dict['doc_count']

            for fos_id in facet_fos_id:
                count = cache.get(fos_id)
                if isinstance(count, int):
                    num += count

            if num == 0:
                papers_num = settings.PAPER_NUM
            else:
                papers_num = num
        return HttpResponse(json.dumps({"data": paper_list, "page_num": math.ceil(papers_num/10),
                                       "result_num": papers_num}))


@csrf_exempt
def get_fos_agg(request):

    search_type = request.POST.get("type", default="").strip()

    # 针对某一特定领域的子领域作聚合,只返回聚合结果
    fos_id = request.POST.get("fos_id", default="")
    if search_type == "advanced":
        title = request.POST.get("title", default="").strip()
        author_name = request.POST.get("author_name", default="").strip()
        author_org = request.POST.get("author_org", default="").strip()
        venue = request.POST.get("venue", default="").strip()
        year = request.POST.get("year", default="").strip()
        keywords = request.POST.get("keywords", default="").strip()
        fos = request.POST.get("fos", default="").strip()
        lang = request.POST.get("lang", default="").strip()
        publisher = request.POST.get("publisher", default="").strip()
        issn = request.POST.get("issn", default="").strip()
        doi = request.POST.get("doi", default="").strip()
        url = request.POST.get("url", default="").strip()
        abstract = request.POST.get("abstract", default="").strip()

        condition = AdvancedSearchCondition(title=title, author_name= author_name, author_org= author_org, venue=venue,
                                        year=year, keywords=keywords, fos=fos, lang=lang, publisher=publisher,
                                        issn=issn, doi=doi, url=url, abstract=abstract)
        agg = FosAggregation(fos_id)

        config = SimpleSearchConfig(size=0)

        search_body = AdvancedSearch(condition=condition, config= config, agg=agg, facet=None).build()
    else:
        info = request.POST.get("search_content", default="")

        condition = GeneralSearchCondition(content=info)

        agg = FosAggregation(fos_id)

        config = SimpleSearchConfig(size=0)

        search_body = GeneralSearch(condition=condition, config=config, agg=agg, facet=None).build()

    if condition.is_empty():

        fos_child = settings.FOS_DICT[fos_id]['child']
        result_list = list()
        for fos in fos_child:
            count = cache.get(fos[0])
            if isinstance(count, int):
                result_list.append({
                    "id": fos[0],
                    "name": fos[1],
                    "count": count,
                })
        return HttpResponse(json.dumps(result_list))

    else:
        result = es.search(index=settings.ELASTIC['INDEX'], body=search_body)
        return HttpResponse(conversion_sub_fos_agg(result, agg.name_id_mapper))
