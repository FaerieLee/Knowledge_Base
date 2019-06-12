# -*-coding:utf-8-*-

import requests
import json
import os

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context


"""
爬取微软学术网站提供的学科层次结构s
"""


class DESAdapter(HTTPAdapter):
	"""
	A TransportAdapter that re-enables 3DES support in Requests.
	"""

	def init_poolmanager(self, *args, **kwargs):
		context = create_urllib3_context(ciphers=CIPHERS)
		kwargs['ssl_context'] = context
		return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

	def proxy_manager_for(self, *args, **kwargs):
		context = create_urllib3_context(ciphers=CIPHERS)
		kwargs['ssl_context'] = context
		return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


def robot(topic_list, topic_dir):
	global s
	if topic_list:
		for topic in topic_list:
			topic_id = topic['id']
			name = str(topic['id'])

			data = {
				"underfosid": int(topic_id)
			}
			response = s.get("https://academic.microsoft.com/api/etap/topicbrowser", params=data)
			response_json = json.loads(response.text)

			if response_json['childTopics']:
				with open(topic_dir + "/" + name, mode="w", encoding="utf-8") as child_topics_writer:
					for child in response_json['childTopics']:
						child_topics_writer.write(json.dumps(child) + "\n")

				robot(response_json['childTopics'], topic_dir)
		return
	else:
		return


# 递归获取微软官网的fos信息
if __name__ == "__main__":

	CIPHERS = (
		'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
		'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
		'!eNULL:!MD5'
	)
	root_topic_path = "level_0_fos"
	topics = []

	with open(root_topic_path) as root_topic:
		lines = root_topic.readlines()

	for line in lines:
		topics.append(json.loads(line))

	os.mkdir("topics")
	os.chdir("./topics")
	thread_list = []

	s = requests.Session()
	s.mount('https://academic.microsoft.com/api/etap/topicbrowser', DESAdapter())

	for spe_topic in topics:
		os.mkdir(spe_topic['name'])
		robot([spe_topic], os.getcwd() + "/" + spe_topic['name'])

	s.close()