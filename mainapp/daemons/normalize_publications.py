import os
import sys
import re
import pymorphy2
import traceback
import psutil
import time
from more_itertools import unique_everseen

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'canonizator'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'canonizator.settings'

from django.conf import settings
import django
django.setup()

from mainapp.models import *
from vocabulary.models import *
from mainapp.daemons.base import Base
from django.db.models import Max

class Program:

	def __init__(self):
		self.name = 'Канонизация'
		self.file_name = 'normalize_publications'
		self.morth = pymorphy2.MorphAnalyzer()

		self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
		self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')
		self.context = Base().create_daemon_context(self.file_name)

		self.punctuations = re.compile('([-_<>?/\\".,{}@#!&()=+:;«»—*])')
		self.grammems_to_remove = {
			'NPRO',
			'PRED',
			'PREP',
			'CONJ',
			'PRCL',
			'INTJ',
			'ROMN',
			'UNKN'
		}

		self.vocabulary = {
            'NOUN': [],
            'ADJF': [],
            'ADJS': [],
            'COMP': [],
            'VERB': [],
            'INFN': [],
            'PRTF': [],
            'PRTS': [],
            'GRND': [],
            'NUMR': [],
            'ADVB': [],
            'LATN': [],
            'NUMB': [],
            'intg': [],
            'real': [],
        }

	def get_last_status(self):
		try:
			max_date = NormalizePublicationStatus.objects.all().aggregate(Max('date'))['date__max']
			last_status = NormalizePublicationStatus.objects.get(date=max_date)
		except:
			last_status = 'no status'
		return last_status

	def get_last_error(self):
		try:
			max_date = NormalizePublicationError.objects.all().aggregate(Max('date'))['date__max']
			last_error = NormalizePublicationError.objects.get(date=max_date)
		except:
			last_error = 'no status'
		return last_error

	def start(self):
		last_pcopy = self.get_last_pcopy_id()
		pcopy_list = self.get_pcopy_list(last_pcopy)
		normalized_list = self.normalize(pcopy_list)
		self.save(normalized_list)
		###############################
		# обработка словаря
		self.__remove_doubles(self.vocabulary)


	#### функция удаления дубликатов значений списков в словаре
	def __remove_doubles(self, vocabulary):
		for key in vocabulary:
			vocabulary[key] = list(unique_everseen(vocabulary[key]))


	def save_error(self):

		Base().connection()
		
		e_type, e_value, e_traceback = sys.exc_info()
		error = NormalizePublicationError.objects.create(
                error = traceback.format_exception(e_type,
                                                    e_value,
                                                    e_traceback)
            )

	def save_status(self, count):

		Base().connection()

		if count > 0:
			status = 'Ok'
		else:
			status = 'Empty'

		NormalizePublicationStatus.objects.create(
				status = status,
				count = count
			)

	def remove_punctuation(self, string):
		string = self.punctuations.sub('', string)
		string = ' '.join(string.splitlines())
		return string

	def split_line(self, line):
		words_list = line.split(' ')
		return words_list

	def parse_to_morph(self, word):
		return self.morth.parse(word)[0]

	def check_word(self, parsed_to_morph):
		if parsed_to_morph.tag.POS in self.grammems_to_remove:
			return False
		else:
			return True

	def normalize_word(self, parsed_to_morph):
		normal_form = parsed_to_morph.normal_form
		# наполненяем словарь каждым встречающимся словом
		self.fill_vocabulary(parsed_to_morph, normal_form)
		return normal_form

	# наполнение словаря
	def fill_vocabulary(self, parsed_to_morph, normal_form):
		pos = parsed_to_morph.tag.POS
		if pos in self.vocabulary:
			self.vocabulary[pos].append(normal_form)


	def get_last_pcopy_id(self):

		Base().connection()
		try:
			last_pcopy = NormalizePublication.objects.all().aggregate( \
				Max('CopyPublication_id'))['CopyPublication_id__max']
		except:
			last_pcopy = None
		return last_pcopy

	def get_pcopy_list(self, last_pcopy):

		Base().connection()

		last_pcopy = self.get_last_pcopy_id()
		if last_pcopy != None:
			pcopy_list = CopyPublication.objects.filter(id__gt=last_pcopy).values( \
				'id', 'title', 'text')[:1]
		else:
			pcopy_list = CopyPublication.objects.all().values('id', 'title', 'text')[:1]
		return pcopy_list

	def normalize(self, pcopy_list):
		for pcopy in pcopy_list:

			pcopy['title'] = self.remove_punctuation(pcopy['title'])
			pcopy['text'] = self.remove_punctuation(pcopy['text'])

			title = []
			for word in self.split_line(pcopy['title']):
				word_parsed_to_morph = self.parse_to_morph(word)
				if self.check_word(word_parsed_to_morph):
					title.append( self.normalize_word(word_parsed_to_morph) )

			pcopy['title'] = ' '.join(title)

			text = []
			for word in self.split_line(pcopy['text']):
				word_parsed_to_morph = self.parse_to_morph(word)
				if self.check_word(word_parsed_to_morph):
					text.append( self.normalize_word(word_parsed_to_morph) )

			pcopy['text'] = ' '.join(text)

		return pcopy_list

	def save(self, normalized_list):

		Base().connection()

		normalized_publications = []
		for item in normalized_list:
			normalized_publications.append(
				NormalizePublication(
					title = item['title'],
					text = item['text'],
					CopyPublication_id = item['id']
				)
			)
		count = len(normalized_publications)
		if count > 0:
			NormalizePublication.objects.bulk_create(normalized_publications)

		self.save_status(count)

	########################################
	# запуск программы
	def run_daemon(self):
		self.start()
		print (self.vocabulary)
		# try:
		# 	self.context.open()
		# 	with self.context:
		# 		while True:
		# 			Base().update_working_status(self, 'waiting')
		# 			can_program = Base().can_program(self)
		# 			if can_program:
		# 				Base().update_working_status(self, 'working')
		# 				self.start()
		# 				Base().update_working_status(self, 'waiting')
		# 				Base().update_pidfile(self)
		# 				time.sleep(300)
		# 			else:
		# 				time.sleep(300)
		# except Exception:
		# 	self.save_error()

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

a = Program().run_daemon()