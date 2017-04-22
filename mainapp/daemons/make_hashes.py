import os
import sys
import traceback
import psutil
import time
import pymorphy2
import binascii
from bulk_update.helper import bulk_update

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'canonizator'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'canonizator.settings'

from django.conf import settings
import django
django.setup()
from django.db.models import Max

from mainapp.models import *
from vocabulary.models import *
from mainapp.daemons.base import Base

class Program:

	def __init__(self):
		self.publications_count = 10
		self.name = 'Создание хешей публикаций'
		self.file_name = 'make_hashes'
		self.morth = pymorphy2.MorphAnalyzer()


		self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
		self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')
		self.context = Base().create_daemon_context(self.file_name)

		self.vocabulary = {
			'NOUN': NOUN,
			'ADJF': ADJF,
			'ADJS': ADJS,
			'COMP': COMP,
			'VERB': VERB,
			'INFN': INFN,
			'PRTF': PRTF,
			'PRTS': PRTS,
			'GRND': GRND,
			'NUMR': NUMR,
			'ADVB': ADVB,
			'LATN': LATN,
			'NUMB': NUMB,
			'intg': intg,
			'real': real,
		}

	def get_last_status(self):

		Base().connection()

		try:
			max_date = MakeHashesStatus.objects.all().aggregate(Max('date'))['date__max']
			last_status = MakeHashesStatus.objects.get(date=max_date)
		except:
			last_status = 'no status'
		return last_status


	def get_last_error(self):

		Base().connection()

		try:
			max_date = MakeHashesError.objects.all().aggregate(Max('date'))['date__max']
			last_error = MakeHashesError.objects.get(date=max_date)
		except:
			last_error = 'no status'
		return last_error

	def save_error(self):

		Base().connection()

		e_type, e_value, e_traceback = sys.exc_info()
		error = MakeHashesError.objects.create(
			error = traceback.format_exception(e_type,
				e_value,
				e_traceback
			)
		)

	def save_status(self, count):

		Base().connection()

		if count > 0:
			status = 'Ok'
		else:
			status = 'Empty'

		MakeHashesStatus.objects.create(
				status = status,
				count = count
			)

	def __get_all_words(self, packet):
		vocabulary = {}
		vocabulary['None'] = []

		for key, value in self.vocabulary.items():
			vocabulary[key] = []

		for line in packet:

			for key, words in line.title_words.items():
				self.__add_in_vocabulary_if_not_exists(key, words, vocabulary)

			for key, words in line.text_words.items():
				self.__add_in_vocabulary_if_not_exists(key, words, vocabulary)

		return vocabulary

	def __add_in_vocabulary_if_not_exists(self, key, words, vocabulary):
		for word in words:
			if not word in vocabulary[key]:
				vocabulary[key].append(word)

	def __replace_synonims(self, vocabulary):

		Base().connection()

		if 'None' in vocabulary:
			del vocabulary['None']

		for key, words in vocabulary.items():

			pos_words = self.vocabulary[key].objects.filter(crc32__in=words).values(
				'id', 'parent_id', 'crc32')

			parent_ids = []

			for pos_word in pos_words:
				parent_ids.append(pos_word['parent_id'])

			pos_parents = self.vocabulary[key].objects.filter(id__in=parent_ids).values(
				'id', 'crc32')

			result = []

			for pos_word in pos_words:
				result_line = {}
				for pos_parent in pos_parents:
					if pos_word['parent_id'] == pos_parent['id']:
						result_line['word_parent'] = pos_parent['crc32']
				result_line['word'] = pos_word['crc32']
				result.append(result_line)

			vocabulary[key] = result

	def __add_parent(self, result, vocabulary):
		for pos, words in vocabulary.items():
			doubled = 0
			for word in words:
				if word['word'] == result['word']:
					if 'word_parent' in word:
						result['word_parent'] = word['word_parent']
						doubled = 1
						break
			if doubled == 0:
				break

	def __link_numbers(self, poses_words, poses_hash, vocabulary):
		result = {}
		for pos, words in poses_words.items():
			result_list = []
			for word in words:
				result_line = {}
				no = self.__find_number(word, poses_hash)
				result_line['word'] = word
				result_line['no'] = no

				# добавляем родителя
				self.__add_parent(result_line, vocabulary)

				result_list.append(result_line)
			result[pos] = result_list
		return result

	def __append_n_sort(self, line_words):
		result = []
		for pos, words in line_words.items():
			if pos != 'None':
				for word in words:
					result.append(word)

		return sorted(result, key=lambda word: word['no'])

	def __make_list_with_parents(self, line_words):
		result = []
		for line_word in line_words:
			if 'word_parent' in line_word:
				result.append(line_word['word_parent'])
			else:
				result.append(line_word['word'])
		return result

	def start(self):

		Base().connection()

		packet = NormalizePublication.objects.filter(
			title_hashes={}
		).order_by('pubdate')[:self.publications_count]

		# запрашиваем все слова
		vocabulary = self.__get_all_words(packet)

		# подтягиваем синонимы
		self.__replace_synonims(vocabulary)

		result = []

		for line in packet:

			result_line = {}

			title = self.__hash_list(line.title.split(' '))
			text = self.__hash_list(line.text.split(' '))
			
			result_line['title_hash'] = title
			result_line['text_hash'] = text

			# цепляем номера к заголовку
			result_line['title_words'] = self.__link_numbers(
				line.title_words, result_line['title_hash'], vocabulary)
			#складываем все слова
			result_line['title_words'] = self.__append_n_sort(result_line['title_words'])
			#создаем лист со словами
			result_line['title_words'] = self.__make_list_with_parents(result_line['title_words'])

			# цепляем номера к тексту
			result_line['text_words'] = self.__link_numbers(
				line.text_words, result_line['text_hash'], vocabulary)
			#складываем все слова
			result_line['text_words'] = self.__append_n_sort(result_line['text_words'])
			#создаем лист со словами
			result_line['text_words'] = self.__make_list_with_parents(result_line['text_words'])

			result.append({
				'id': line.id,
				'title_hashes': result_line['title_words'],
				'text_hashes': result_line['text_words'],
			})

		for line in packet:
			for result_line in result:
				if line.id == result_line['id']:
					line.title_hashes = result_line['title_hashes']
					line.text_hashes = result_line['text_hashes']

		bulk_update(packet)

		self.save_status(len(packet))

	def __append_numbers(self, list_words):
		result_list = []
		for pos, words in list_words.items():
			result_line = []
			for word in words:
				no = self.__find_number(word, list_words['title_has'])

	def __find_number(self, word_to_find, words_list):
		for key, word in enumerate(words_list):
			if word_to_find == word:
				return key

	def __hash_list(self, words_list):
		crc32 = []
		for word in words_list:
			crc32.append(binascii.crc32(bytes(word, 'utf-8')))
		return crc32

	def delete_hashes(self):

		to_delete = NormalizePublication.objects.exclude(title_hashes={}).update(
			title_hashes={},
			text_hashes={},
		)

	########################################
	# запуск программы
	def run_daemon(self):
		try:
			self.context.open()
			with self.context:
				while True:
					Base().update_working_status(self, 'waiting')
					can_program = Base().can_program(self)
					if can_program:
						Base().update_working_status(self, 'working')
						self.start()
						Base().update_working_status(self, 'waiting')
						Base().update_pidfile(self)
						time.sleep(300)
					else:
						time.sleep(300)
		except Exception:
			self.save_error()

	def get_pid(self):

		processes = psutil.pids()

		directory = self.pids_dir
		pid_file = open(os.path.join(directory, '{0}.pid'.format(self.file_name)), "r")  

		with pid_file:
			pid_value = int(pid_file.readlines()[0])

			pid_file.close()

			if pid_value in processes:
				return pid_value
			else:
				os.remove(os.path.join(directory, '{0}.pid'.format(self.file_name)))
				return None
    #############################################