# -*-coding:utf-8-*-
import os
import json

from Knowledge_base.search.utils.fos_init import init_fos

"""
 测试solr数据的学科在学科树上出现的比例
"""

current_path = '/home/ziqi/PycharmProjects/Knowledge_base'
topics_dir = os.path.join(current_path,"data/level_0_fos")
fos_dir = os.path.join(current_path, "data/fos")
fos_set = set()

# root_fos, fos_dict: format:{ "fos_id":{“name”:name1, "child":[]},....}
root_fos, fos_dict = init_fos(topics_dir, fos_dir)

print('the length of fos including id : ' + str(len(fos_dict)))

fos_name = fos_dict.values()

print('the length of fos including name : ' + str(len(fos_name)))

for ele in fos_name:
	if 'name' in ele:
		fos_set.add(str(ele['name']).lower().strip())

print('the length of fos set : ' + str(len(fos_set)))

solr_data_path = '/home/ziqi/文档/solrData/solr-import-export-json/tmp/collection.json'
all_fos = 0
exit_fos = 0
error_num = 0
solr_fos_set = set()
exit_fos_set = set()

with open(solr_data_path) as solr_file:
	for line in solr_file.readlines():
		try:
			fields = json.loads(line)
			if 'subject' in fields:
				for ele in fields['subject']:
					fos = str(ele).lower().strip()
					solr_fos_set.add(fos)
					if fos in fos_set:
						exit_fos += 1
						exit_fos_set.add(fos)
					all_fos += 1
		except json.decoder.JSONDecodeError as e:
			print(line)
			error_num += 1
			continue

print('the number of existing fos : ' + str(exit_fos))

print('the number of solr all fos : ' + str(all_fos))

print('the ratio : ' + str(exit_fos/all_fos))

print('error num : ' + str(error_num))

print(len(exit_fos_set)/len(solr_fos_set))

print('solr fos set num : ' + str(len(exit_fos_set)))
