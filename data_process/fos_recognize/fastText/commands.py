#-*-coding:utf-8-*-


import os
import subprocess
import sys
from multiprocessing.pool import Pool
import copy

from tabulate import tabulate


def train(train_set_url, result_url):

	epoch = 10

	while epoch <= 30:
		lr = 0.01
		while lr <= 0.3:
			ngram = 1

			while ngram <= 2:

					command_str = '/opt/fastText/fasttext supervised'
					for train_set in os.listdir(train_set_url):
						train_url = os.path.join(train_set_url, train_set)
						input_url = ' -input ' + train_url + ' -output '
						dest_url = '/opt/models/'
						model_url = 'model_e' + str(epoch) + '_' + 'lr' + str(lr) + '_' \
							+ 'ngram' + str(ngram) + '_' + 'fos' + train_set[0]
						paras = ' -epoch ' + str(epoch) + ' -lr ' + str(lr) + ' -thread 24 -wordNgrams ' + str(ngram) +\
							' -loss one-vs-all'
						command = command_str + input_url + dest_url + model_url + paras

						with open(os.path.join(result_url, model_url + '_process.txt'), mode="w") as process_writer:
							result = subprocess.getoutput(command)
							process_writer.write(result)

					ngram += 1

			if lr == 0.01:
				lr = 0.05
			elif lr == 0.05:
				lr += 0.05
			else:
				lr += 0.1
		epoch += 10


def test(model_url):

	rate = 0.5
	while rate < 0.8:

		test_command_str = '/opt/fastText/fasttext test.txt '

		val_url = os.path.join('/opt/val_set', model_url.spit('_')[-1] + '_val_set.txt')

		train_url = os.path.join('/opt/train_set', model_url.spit('_')[-1] + '_train_set.txt')

		test_train_command = test_command_str + '/opt/models/' + model_url + '.bin ' + train_url + ' -1 ' + str(rate)
		test_val_command = test_command_str + '/opt/models/' + model_url + '.bin ' + val_url + ' -1 ' + str(rate)

		with open(os.path.join('/opt/result', model_url + '_' + str(rate) + '_train.txt'), mode="w") as train_writer:
			test_train_result = subprocess.getoutput(test_train_command)
			train_writer.write(test_train_result)

		with open(os.path.join('/opt/result', model_url + '_' + str(rate) + '_val.txt'), mode="w") as val_writer:
			test_val_result = subprocess.getoutput(test_val_command)
			val_writer.write(test_val_result)

		rate += 0.05


def conversion_result(directory):

	result_dict = dict()
	for sub in os.listdir(directory):
		eles = sub.split('_')
		if 'model_e10' in sub and 'val' in sub and '3' in eles[4]:
			elements = sub.split('_')
			lr = elements[2][2:6]
			ngram = elements[3][5:]
			result_str = ''
			with open(os.path.join(directory, sub), mode="r") as val_reader:

				count = 0
				for line in val_reader:
					if count == 1:
						result_str = result_str + line[4:].strip()
					elif count == 2:
						result_str = result_str + '/' + line[4:].strip()
					count += 1
				result_dict[str(lr) + '_' + str(ngram) + '_' + str(elements[5][:4])] = result_str
	sort_dict = sorted(result_dict)

	print(sort_dict)

	count = 0
	result_list = []
	table = []
	headers = ['lr/ngram', '0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9']
	for k in sort_dict:
		if count == 8:

			result_list.append(result_dict[k])
			table.append(copy.deepcopy(result_list))
			result_list.clear()
			count = 0
		elif count == 0:
			result_list.append(k[:6])
			result_list.append(result_dict[k])
			count += 1
		else:
			result_list.append(result_dict[k])
			count += 1
	print(tabulate(table, headers, tablefmt="plain"))


# ps -ef|grep python3


if __name__ == "__main__":

	conversion_result("/home/ziqi/桌面/result")
	# pool = Pool(processes=8)
	#
	# models_url = sys.argv[1]
	#
	# model_set = set()
	#
	# for model_url in os.listdir(models_url):
	#
	# 	model_set.add(model_url[:-4])
	#
	# for model in model_set:
	# 	pool.apply(test.txt, model)
	#
	# pool.close()
	# pool.join()
