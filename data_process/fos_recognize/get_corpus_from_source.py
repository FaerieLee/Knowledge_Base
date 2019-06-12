# -*-coding:utf-8-*-

import sys
import threading
from os import listdir
import os
import json

import nltk
from nltk.corpus import stopwords as pw
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer


STOP_WORDS = pw.words("english")


def get_original_corpus(source_dir, corpus_url):
	count = 0
	with open(corpus_url, mode="w") as writer:
		for file_name in listdir(source_dir):
			if 'mag_papers' in file_name:
				with open(os.path.join(source_dir, file_name), mode="r") as reader:
					for line in reader:
						elements = json.loads(line)
						if 'fos' in elements and 'abstract' in elements and 'title' in elements:
							writer.write(line)
					count += 1
					print(count)


def merge_file(directory, file_url):
	with open(file_url, mode="w") as writer:
		for file in os.listdir(directory):
			with open(os.path.join(directory, file), mode="r") as reader:
				for line in reader:
					writer.write(line)


def get_fos_corpus(original_corpus_url, fos_url, fos_corpus_url):
	fos_set = set()
	with open(fos_url, mode="r") as reader:
		for line in reader:
			fos_set.add(json.loads(line)['name'])

	with open(original_corpus_url, mode="r") as reader, open(fos_corpus_url, mode="w") as writer:
		for line in reader:
			elements = json.loads(line)
			if len(set(elements['fos']) & fos_set) == 1:
				writer.write(line)


def get_en_corpus(original_url, corpus_url):
	with open(original_url, mode="r") as reader, open(corpus_url, mode="w") as writer:
		for line in reader:
			elements = json.loads(line)
			if 'lang' in elements and elements['lang'] == 'en':
				writer.write(line)


def delete_stop_words(original_url, stop_words, corpus_url):

	with open(original_url, mode="r") as reader, open(corpus_url, mode="w") as writer:
		for line in reader:
			elements = json.loads(line)
			word_tokens = nltk.word_tokenize(elements['title'] + ' ' + elements['abstract'])
			word_list = [w.lower() for w in word_tokens if not w.lower() in stop_words]
			tmp = dict()
			tmp['fos'] = elements['fos']
			tmp['words'] = simple_process(word_list)
			writer.write(json.dumps(tmp) + os.linesep)


def multi_thread_delete_stop_words(original_directory, corpus_directory):
	for file in os.listdir(original_directory):
		stop_words = pw.words("english")
		t = threading.Thread(target=delete_stop_words, args=(original_directory+file, stop_words, corpus_directory+file))
		t.start()


def simple_process(word_list):
	tmp = ""
	for word in word_list:
		if len(word) > 1:
			tmp = tmp + word + ' '
	return tmp


def judge_train_val_percentage(train_url, val_url):
	with open(train_url, mode="a") as train_writer, open(val_url, mode="r") as reader, open("val_new.txt", mode="w") as val_writer:
		count = 0
		for line in reader:
			if count < 600000:
				train_writer.write(line)
				count += 1
			else:
				val_writer.write(line)


def get_word2vec_corpus(directory, dest_url):
	with open(dest_url, mode="w") as writer:
		for sub in os.listdir(directory):
			with open(os.path.join(directory, sub), mode="r") as reader:
				for line in reader:
					elements = json.loads(line)
					writer.write(elements['words'] + os.linesep)


if __name__ == "__main__":

	get_word2vec_corpus(sys.argv[1], sys.argv[2])
#	judge_train_val_percentage(sys.argv[1], sys.argv[2])
#	lemmatizer = WordNetLemmatizer()
#	print(lemmatizer.lemmatize('played', pos=''))
#	stemmer = PorterStemmer()
#	print(stemmer.stem('playing'))
