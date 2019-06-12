#  -*-coding:utf-8-*-
from selenium import webdriver
import time
import sys
import json
import random

browser = webdriver.Firefox()

browser.maximize_window()  # 最大化窗口
test_case_path = sys.argv[1]

interval = 5

browser.get("http://172.31.34.105:8000")
with open(test_case_path, mode="r") as test_cases:
	for test_case in test_cases:
		paras = json.loads(test_case)
		if paras["type"] == "advanced":
			pass
		else:
			time.sleep(interval)
			browser.find_element_by_id("kw").send_keys(paras['content'])
			time.sleep(interval)
			browser.find_element_by_id("su").click()
			time.sleep(interval)

	# 将页面滚动条拖到底部
	js_down = "document.documentElement.scrollTop=10000"
	browser.execute_script(js_down)
	time.sleep(interval)

	# 将滚动条移动到页面的顶部
	js_up = "document.documentElement.scrollTop=0"
	browser.execute_script(js_up)
	time.sleep(interval)

	papers = browser.find_element_by_id("papers")
	time.sleep(interval)

	# 向后翻页，向前翻页，随机翻页
	page_count = 0
	while page_count < 2:
		browser.find_element_by_id("next_page").click()
		page_count += 1
		time.sleep(interval)
		browser.execute_script(js_down)
		time.sleep(interval)

	page_count = 0
	while page_count < 2:
		browser.find_element_by_id("previous_page").click()
		page_count += 1
		time.sleep(interval)
		browser.execute_script(js_down)
		time.sleep(interval)

	page_count = 0
	while page_count < 2:
		pages = browser.find_element_by_id("page_list")
		pages[random.randint(0,len(pages))].click()
		page_count += 1
		time.sleep(interval)
		browser.execute_script(js_down)
		time.sleep(interval)


	#领域搜索:年份
	years = browser.find_elements_by_id("menu_year")
	if years:
		years[0].click()
		time.sleep(interval)
		years[0].click()
		time.sleep(interval)

	# 领域搜索：学科
	years = browser.find_elements_by_id("menu_year")
	if years:
		years[0].click()
		time.sleep(interval)
		years[0].click()
		time.sleep(interval)

	# 领域搜索：作者名字
	years = browser.find_elements_by_id("menu_year")
	if years:
		years[0].click()
		time.sleep(interval)
		years[0].click()
		time.sleep(interval)

	# 领域搜索：出版社
	years = browser.find_elements_by_id("menu_year")
	if years:
		years[0].click()
		time.sleep(interval)
		years[0].click()
		time.sleep(interval)

	# 排序：
	browser.find_element_by_id("sort_list").click()
	time.sleep(interval)
	browser.find_element_by_id("year_sort").click()
	time.sleep(interval)
	browser.find_element_by_id("sort_list").click()
	time.sleep(interval)
	browser.find_element_by_id("citation_sort").click()
	time.sleep(interval)

	# 查看论文详情,原始链接：
	if papers:
		links = papers.find_element_by_tag_name("a")

		# 查看原始链接
		if len(links) > 0:
			links[0].click()
			time.sleep(interval)

		# 返回原页面
		browser.back()

		#查看论文详情
		links[0].click()
		time.sleep(interval)

	# 摘要点击：

