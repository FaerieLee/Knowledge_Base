# -*-coding:utf-8-*-

import os
import subprocess
import sys

from tabulate import tabulate


def main():

	epoch = 10

	while epoch <= 50:
		lr = 0.01
		while lr <= 0.3:
			ngram = 1

			while ngram <= 3:

					original_train_command = '/home/17126189/install_pack/fastText/fastText/fasttext supervised -input /data/word2vec/corpus/no_stopwords_4-1/train_set -output '
					dest_url = '/data/word2vec/corpus/no_stopwords_4-1/'
					model_url = 'model_e' + str(epoch) + '_' + 'lr' + str(lr) + '_' + 'ngram' + str(ngram)
					paras = ' -epoch ' + str(epoch) + ' -lr ' + str(lr) + ' -thread 24 -wordNgrams ' + str(ngram)
					command = original_train_command + dest_url + model_url + paras
					os.mkdir('/'+ dest_url + model_url)

					print(command)

					with open('/' + dest_url + model_url + '/process.txt', mode="w") as process_writer:
						result = subprocess.getoutput(command)
						process_writer.write(result)

					test_train_command = '/home/17126189/install_pack/fastText/fastText/fasttext test.txt /data/word2vec/corpus/no_stopwords_4-1/' + \
						model_url + '.bin ' + '/data/word2vec/corpus/no_stopwords_4-1/train_set'
					test_val_command = '/home/17126189/install_pack/fastText/fastText/fasttext test.txt /data/word2vec/corpus/no_stopwords_4-1/' + \
						model_url + '.bin ' + '/data/word2vec/corpus/no_stopwords_4-1/val_set'
					with open(dest_url + model_url + '/train.txt', mode="w") as train_writer:
						test_train_result = subprocess.getoutput(test_train_command)
						train_writer.write(test_train_result)

					with open(dest_url + model_url + '/val.txt', mode="w") as val_writer:
						test_val_result = subprocess.getoutput(test_val_command)
						val_writer.write(test_val_result)

					ngram += 1

			if lr == 0.01:
				lr = 0.05
			else:
				lr += 0.05
		epoch += 10


def conversion_result(directory):

	result_dict = dict()
	for sub in os.listdir(directory):
		sub_dir = os.path.join(directory,sub)
		if os.path.isdir(sub_dir) and 'model_e10' in sub:
			elements = sub.split('_')
			lr = elements[2][2:6]
			ngram = elements[3][5:]
			result_str = ''
			with open(os.path.join(sub_dir,'train.txt'), mode="r") as train_reader, open(os.path.join(sub_dir,'val.txt'), mode="r") as val_reader:
				count = 0
				for line in train_reader:
					if count == 1:
						result_str = result_str + line[3:].strip() + ' / '
					count += 1

				count = 0
				for line in val_reader:
					if count == 1:
						result_str = result_str + line[3:].strip()
					count += 1
				result_dict['123'] = result_str
	sort_dict = sorted(result_dict)

	count = 0
	result_list = ['0.01']
	table = []
	headers = ['lr/ngram', '1', '2', '3']
	for k in sort_dict:
		if count == 2:

			result_list.append(result_dict[k])
			table.append(result_list)
			if result_list[0] == '0.01':
				result_list = ['0.05']
			else:
				tmp = float(result_list[0]) + 0.05
				result_list = [str(tmp)]
			count = 0
		else:
			result_list.append(result_dict[k])
			count += 1
	print(tabulate(table, headers, tablefmt="plain"))

if __name__ == "__main__":
	conversion_result(sys.argv[1])



