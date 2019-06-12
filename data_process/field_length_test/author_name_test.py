# -*-coding:utf-8-*-
from os import listdir
import json
import sys
import os

"""
读取Aminer原始文件，通过判断字段长度，获取异常数据
"""

if __name__ == "__main__":
	# sys.argv传入的参数为字符串类型，如果想做一些条件判断的话需要转成你所需要的数据类型

	directory = sys.argv[1]  # 存放文件的文件夹位置

	dest_content_file = "./content_length.txt"
	dest_length_file = "./name_length.txt"

	file_names = listdir(directory)  # 列出该文件夹下所有文件

	with open(dest_length_file, mode='w') as dest_length, open(dest_content_file, mode='w') as dest_content:
		for file_name in file_names:
			count = 0
			if 'aminer_papers_' in file_name:
				with open(os.path.join(directory, file_name), encoding="utf-8", mode="r") as line_list:
					for line in line_list:  # 默认一行 为 一条数据
						try:
							fields = json.loads(line)
							if 'authors' in fields:
								for author in fields['authors']:
									if 'name' in author and isinstance(author['name'], str):
										name_len = len(author['name'])
										if name_len > 500:
											dest_content.write(line)
										if name_len > count:
											count = len(author['name'])

						except json.decoder.JSONDecodeError as e:
							# 可能会遇到解析json数据错误,对于此类数据,忽略而过
							print(file_name)
							continue

				dest_length.write(file_name + ':' + str(count) + os.linesep)
