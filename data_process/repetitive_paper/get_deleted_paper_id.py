# -*-coding:utf-8-*-

import sys
import os

"""
作用：处理spark输出的相同doi的文章id文件,并产出 需删除id文件, 以及 未删除id->需删除id的映射文件
处理流程：
1.读取目录下spark产出的一系列文件
2.以id中是否包含'-'字符判断paper来自于aminer还是mag,优先删除aminer中的paper
3.生成 需删除id文件以及映射文件
数据格式：
spark文件数据格式：每行格式为：id id id ....
删除方式：
将诸多ｉｄ中出现在mag数据集中的第一个ｉｄ保留，其余都删除，如果ｉｄ全部没有出现在mag数据集中，则保留第一个，删除其余所有
"""

if __name__ == '__main__':

	file_directory = sys.argv[1]
	deleted_id_file = sys.argv[2]
	relation_id_file = sys.argv[3]

	with open(deleted_id_file, mode="w", encoding="utf-8") as deleted, open(relation_id_file,
																			mode="w", encoding="utf-8") as relations:
		for sub_file in os.listdir(file_directory):
			if sub_file.find('part-') != -1:
				try:
					with open(os.path.join(file_directory, sub_file), mode='r') as source_file:
						for line in source_file:
							id_array = line.strip().split(' ')
							index = 0
							for id in id_array:
								if '-' in id:
									break
								else:
									index += 1

							length = len(id_array)

							if index >= length:
								index = 0

							for i in range(length):
								if i != index:
									relations.write(id_array[i] + ' ' + id_array[index] + os.linesep)
									deleted.write(id_array[i] + os.linesep)
				except UnicodeDecodeError as e:
					print(e)
					print(sub_file)
