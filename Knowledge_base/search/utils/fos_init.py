#-*-coding:utf-8-*-

import json
from copy import deepcopy
import os


def get_child(fos_id, fos_dict,):
	try:
		with open(fos_id) as reader:
			for line in reader.readlines():
				line_json = json.loads(line)
				fos_dict[str(line_json['id'])] = {
					"name": line_json['name'].lower(),
					"child": []
				}
				fos_dict[fos_id]['child'].append((str(line_json['id']), line_json['name'].lower()))
				get_child(str(line_json['id']), fos_dict)
	except FileNotFoundError:
		return


# topics_dir 一级主题的文件, fos_dir 主题的根目录
def init_fos(topics_path, fos_dir):

	root_fos = dict() # 一级主题

	with open(topics_path) as reader:
		for line in reader.readlines():
			fos = json.loads(line)
			root_fos[str(fos['id'])] = {
				"name": fos['name'].lower(),
				"child": []
			}

	fos_dict = deepcopy(root_fos)

	for fos_id in root_fos:
		dir_name = root_fos[fos_id]['name']
		os.chdir(os.path.join(fos_dir, dir_name)) # 将当前路径设置为一级主题的路径
		get_child(fos_id, fos_dict)
		os.chdir(fos_dir) # 讲当前路径设置为主题的根目录

	return root_fos, fos_dict
