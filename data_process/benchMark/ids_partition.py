# -*-coding:utf-8-*-
import sys


if __name__ == "__main__":

	source_path = "/home/ziqi/文档/文件/id_random.txt"
	aminer_path = "/home/ziqi/文档/文件/aminer_random_ids.txt"
	mag_path = "/home/ziqi/文档/文件/mag_random_ids.txt"

	with open(source_path, mode="r") as source, open(aminer_path, mode="w") as aminer:
		with open(mag_path, mode="w") as mag:
			for id in source:
				if '-' in id:
					mag.write(id)
				else:
					aminer.write(id)
