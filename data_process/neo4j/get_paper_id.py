# -*-coding:utf-8-*-

import os
import sys
import json


# 将原有 josn 格式的paper数据->id, name 合适的数据,以供于neo4j导入.
if __name__ == '__main__':

	file_directory = sys.argv[1]
	destination_file = sys.argv[2]

	with open(destination_file, mode="w", encoding="utf-8") as dtnf:
		for sub_file in os.listdir(file_directory):
			if sub_file.find('mag_papers_') != -1 or sub_file.find('aminer_papers_') != -1:
				with open(os.path.join(file_directory, sub_file), mode='r') as source_file:
					for line in source_file:
						try:
							tmp = json.loads(line)
							if 'id' in tmp and 'doi' in tmp:
								dtnf.write(tmp['id'] + ',' + tmp['doi'] +os.linesep)
						except json.decoder.JSONDecodeError as e:
							print(sub_file, e)
							continue
