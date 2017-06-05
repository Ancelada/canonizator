import os
import sys
import re
import pymorphy2
import traceback
import psutil
import time
import binascii
from django.utils import timezone
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
		self.list_value = 400
		self.name = 'Канонизация'
		self.file_name = 'normalize_publications'
		self.morth = pymorphy2.MorphAnalyzer()

		self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
		self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')
		self.context = Base().create_daemon_context(self.file_name)

		self.punctuations = re.compile('([-_<>?/\\".„”“%,{}@#!&()=+:;«»—$&£*])')
		self.replace_with_spaces = {
			'\n',
			'\r',
			'\r\n',
			'\v',
			'\x0b',
			'\f',
			'\x0c',
			'\x1c',
			'\x1d',
			'\x1e',
			'\x85',
			'\u2028',
			'\u2029',
			'<br>',
			'<br />'
			'<p>',
			'</p>',
			'...',
			'\t',
			'\xa0',
			'&nbsp',
			' ',
		}
		self.copypublication_fields = [
			'crawler_id',
			'name',
			'name_cyrillic',
			'title',
			'text',
			'author',
			'date',
			'id',
		]


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

		self.grammems_to_remove_vocabulary = {
			'NPRO': [],
			'PRED': [],
			'PREP': [],
			'CONJ': [],
			'PRCL': [],
			'INTJ': [],
			'ROMN': [],
			'UNKN': [],			
		}

		self.grammems_to_remove_models = {
			'NPRO': NPRO,
			'PRED': PRED,
			'PREP': PREP,
			'CONJ': CONJ,
			'PRCL': PRCL,
			'INTJ': INTJ,
			'ROMN': ROMN,
			'UNKN': UNKN,
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

		self.voc_models = {
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
			max_date = NormalizePublicationStatus.objects.all().aggregate(Max('date'))['date__max']
			last_status = NormalizePublicationStatus.objects.get(date=max_date)
		except:
			last_status = 'no status'
		return last_status

	def get_last_error(self):
		Base().connection()
		try:
			max_date = NormalizePublicationError.objects.all().aggregate(Max('date'))['date__max']
			last_error = NormalizePublicationError.objects.get(date=max_date)
		except:
			last_error = 'no status'
		return last_error

	def __clear_vocabulary(self, vocabulary):
		for key, value in vocabulary.items():
			del vocabulary[key][:]

	def start(self):
		last_pcopy = self.get_last_pcopy_id()
		pcopy_list = self.get_pcopy_list(last_pcopy)
		normalized_list = self.normalize(pcopy_list)
		self.save(normalized_list)

		###############################
		# обработка словаря
		self.__remove_doubles(self.vocabulary)
		self.__remove_already_have(self.vocabulary)
		self.__add_vocabulary_to_db(self.vocabulary)

		self.__clear_vocabulary(self.vocabulary)

		# записываем граммемы to remove
		self.__remove_already_have_grammems_to_remove(self.grammems_to_remove_vocabulary)
		self.__add_vocabulary_grammems_to_remove_to_db(self.grammems_to_remove_vocabulary)

		self.__clear_vocabulary(self.grammems_to_remove_vocabulary)


	#### функция удаления дубликатов значений списков в словаре
	def __remove_doubles(self, vocabulary):
		for key in vocabulary:
			vocabulary[key] = list(unique_everseen(vocabulary[key]))

	### функция удаления уже имеющихся в БД
	def __remove_already_have_grammems_to_remove(self, grammems_to_remove):
		
		Base().connection()

		for key, value in grammems_to_remove.items():
			doubles = self.grammems_to_remove_models[key].objects.filter(
				crc32__in=[word['crc32'] for word in grammems_to_remove[key]]).values('crc32')

			for double in doubles:
				for key2, word in enumerate(value):
					if word['crc32'] == double['crc32']:
						del value[key2]
						break

	#### функция удаления уже имеющихся в БД
	def __remove_already_have(self, vocabulary):

		Base().connection()

		for key, value in vocabulary.items():
			doubles = self.voc_models[key].objects.filter(
				name__in=vocabulary[key]).values('name')
			for double in doubles:
				self.__remove_from_array_by_value(vocabulary[key], double['name'])

	##### удаление из массива по значению
	def __remove_from_array_by_value(self, array, value):
		if value in array:
			array.remove(value)

	##### добавление в БД списков частей речи на удаление
	def __add_vocabulary_grammems_to_remove_to_db(self, grammems_to_remove):

		Base().connection()

		for key in grammems_to_remove:
			words = []
			for word in grammems_to_remove[key]:
				words.append(self.grammems_to_remove_models[key](
					name=word['word'],
					crc32=word['crc32'],
					)
				)
			if len(words) > 0:
				now = timezone.now()
				self.grammems_to_remove_models[key].objects.bulk_create(words)

	##### добавление в БД списков частей речи
	def __add_vocabulary_to_db(self, vocabulary):

		Base().connection()

		for key in vocabulary:
			words = []
			for word in vocabulary[key]:
				words.append(self.voc_models[key](
					name=word,
					crc32=self.__convert_crc32(word),
					)
				)
			if len(words) > 0:
				now = timezone.now()
				self.voc_models[key].objects.bulk_create(words)

	def __convert_crc32(self, value):
		value_bytes=bytes(value, 'utf-8')
		return binascii.crc32(value_bytes)

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
		for key in self.replace_with_spaces:
			string = string.replace(key, ' ')
		string = re.sub(self.punctuations, '', string)
		string = string.replace('ё', 'е')
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
		##### нужно уменьшить размер слова, заменить буквы ё на е
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
			pcopy_list = CopyPublication.objects.filter(id__gt=last_pcopy).values(
				*self.copypublication_fields
			)[:self.list_value]
		else:
			pcopy_list = CopyPublication.objects.all().values(
				*self.copypublication_fields
			)[:self.list_value]
		return pcopy_list

	def normalize(self, pcopy_list):
		for pcopy in pcopy_list:

			pcopy['title'] = self.remove_punctuation(pcopy['title'])
			pcopy['text'] = self.remove_punctuation(pcopy['text'])

			title = []
			title_words = {}
			self.__check_n_normalize(title, title_words, self.split_line(pcopy['title']))
			pcopy['title'] = ' '.join(title)
			pcopy['title_words'] = title_words

			text = []
			text_words = {}
			self.__check_n_normalize(text, text_words, self.split_line(pcopy['text']))
			pcopy['text'] = ' '.join(text)
			pcopy['text_words'] = text_words

		return pcopy_list

	def __check_n_normalize(self, exp_list, exp_voc_list, words):
		for word in words:
			word_parsed_to_morph = self.parse_to_morph(word)
			if self.check_word(word_parsed_to_morph):

				normalized_word = self.normalize_word(word_parsed_to_morph) 
				word_crc_32 = self.__convert_crc32(normalized_word)

				# обычный список нормализованных слов
				exp_list.append( normalized_word )

				# словарь частей речи со словами crc32
				pos = str(word_parsed_to_morph.tag.POS)

				if not pos in exp_voc_list:
					exp_voc_list[pos] = [word_crc_32]
				else:
					exp_voc_list[pos].append(word_crc_32)
			# заполняем словарь частей речи, не учавствующих в разборе нечетких дублей
			else:
				
				normalized_word = self.normalize_word(word_parsed_to_morph)
				word_crc_32 = self.__convert_crc32(normalized_word)

				pos = str(word_parsed_to_morph.tag.POS)

				if not any(voc_word['word'] == normalized_word \
				 for voc_word in self.grammems_to_remove_vocabulary[pos]):
					self.grammems_to_remove_vocabulary[pos].append({
						'word': normalized_word, 'crc32': word_crc_32
					})

	def save(self, normalized_list):

		Base().connection()

		normalized_publications = []
		for item in normalized_list:
			normalized_publications.append(
				NormalizePublication(
					crawler_id = item['crawler_id'],
					name = item['name'],
					name_cyrillic = item['name_cyrillic'],
					title = item['title'],
					text = item['text'],
					author = item['author'],
					pubdate = item['date'],
					CopyPublication_id = item['id'],
					title_words = item['title_words'],
					text_words = item['text_words'],
				)
			)
		count = len(normalized_publications)
		if count > 0:
			NormalizePublication.objects.bulk_create(normalized_publications)

		self.save_status(count)

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