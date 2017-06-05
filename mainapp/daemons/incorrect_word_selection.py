import os
import sys
import traceback
import psutil
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'canonizator'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'canonizator.settings'

from django.conf import settings
import django
django.setup()

from vocabulary.models import *
from django.db.models import Max
from mainapp.daemons.vikidict_corr.vikidict_corr import VikidictCorr
from mainapp.daemons.base import Base

class Program:

	def __init__(self):
		self.name = 'Поиск некорректных слов'
		self.file_name = 'incorrect_word_selection'

		self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
		self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')
		self.context = Base().create_daemon_context(self.file_name)

		self.list_value = 10
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
		self.words_checked_count = None

	def get_last_status(self):

		Base().connection()

		try:
			max_date = IncorrectStatus.objects.all().aggregate(Max('date'))['date__max']
			last_status = IncorrectStatus.objects.get(date=max_date)
		except:
			last_status = 'no status'
		return last_status

	def get_last_error(self):

		Base().connection()

		try:
			max_date = IncorrectError.objects.all().aggregate(Max('date'))['date__max']
			last_error = IncorrectError.objects.get(date=max_date)
		except:
			last_error = 'no status'
		return last_error

	def save_error(self):

		Base().connection()
		
		e_type, e_value, e_traceback = sys.exc_info()
		error = IncorrectError.objects.create(
                error = traceback.format_exception(e_type,
                                                    e_value,
                                                    e_traceback)
            )

	def save_status(self, count):

		Base().connection()

		if not count is None:
			status = 'Ok'
		else:
			status = 'Empty'
			count = 0

		IncorrectStatus.objects.create(
				status = status,
				count = count
			)

	def start(self):

		Base().connection()

		for key, table in self.voc_models.items():
			words = table.objects.filter(
				vikidict_correction_tested=False,
				Tone__isnull=True,
			)[:self.list_value]

			if len(words) > 0:
				result = VikidictCorr().start(words)
				self.update_db(table, result)

		# сохраняем количество обработанных слов 
		self.save_status(self.words_checked_count)

		self.words_checked_count = None

	def update_db(self, table, result):
		#записываем синонимы
		words_ids = []

		for line in result:
			word = table.objects.filter(id=line['id'])
			word.update(
				vikidict_correction_tested = True,
				Tone=line['result'],
			)
			words_ids.append(line['id'])

		if self.words_checked_count == None:
			self.words_checked_count = len(words_ids)
		else:
			self.words_checked_count+=len(words_ids)

	# функция очищения всех словарей
	def clear_vocabulary(self):
		Base().connection()

		for key, value in self.voc_models.items():
			value.objects.all().delete()

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