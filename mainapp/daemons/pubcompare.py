import os
import sys
import traceback
import psutil
import time
from bulk_update.helper import bulk_update

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'canonizator'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'canonizator.settings'

from django.conf import settings
from django.utils import timezone
import django
django.setup()
from django.db.models import Max

from mainapp.models import *
from mainapp.daemons.base import Base

class PubCompare():

	def __init__(self):
		self.status = {
			'unique': {
				'coefficient': {
					'min': 0,
					'max': 39,
				},
				'db_value': 1,
			},

			'reprint': {
				'coefficient': {
					'min': 40,
					'max': 69,
				},
				'db_value': 2,
			},

			'copy': {
				'coefficient': {
					'min': 70,
					'max': 200,
				},
				'db_value': 3,
			},
		}

		self.shingle_length = 3

	def __make_shingles_list(self, source):

		result = []

		for key, value in enumerate(source):

			hash_key_min = key
			hash_key_max = key+self.shingle_length

			if hash_key_max < len(source)+1:

				shingle_item = []

				for i in range(hash_key_min, hash_key_max, 1):
					shingle_item.append(source[i])

				result.append(shingle_item)

		return result

	def compaire(self, source_1, source_2):
		same = 0

		shingles_source_1 = self.__make_shingles_list(source_1)

		shingles_source_2 = self.__make_shingles_list(source_2)


		if len(shingles_source_1) > 0 and len(shingles_source_2) > 0:
			for shingle in shingles_source_1:
				if shingle in shingles_source_2:
					same+=1
			return same*2/float(len(shingles_source_1) + len(shingles_source_2))*100
		else:
			return 0

	def get_status(self, pub_1_line, pub_2_line):

		text_weight = self.compaire(
			pub_1_line.text_hashes,
			pub_2_line['text_hashes'])*0.8

		title_weight = self.compaire(
			pub_1_line.title_hashes,
			pub_2_line['title_hashes'])*0.2

		result = round(text_weight + title_weight)

		for key, value in self.status.items():

			if result >= self.status[key]['coefficient']['min'] and \
			 result <= self.status[key]['coefficient']['max']:

			 	status = key

		return {
			'coefficient': result,
			'status': status,
		}

class Program():

	def __init__(self):
		self.pub_without_status_length = 100
		self.retrospective_days_delta = 10
		self.name = 'Поиск нечетких дубликатов'
		self.file_name = 'pubcompare'

		self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
		self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')
		self.context = Base().create_daemon_context(self.file_name)

	def get_last_status(self):

		Base().connection()

		try:
			max_date = PubCompareStatus.objects.all().aggregate(Max('date'))['date__max']
			last_status = PubCompareStatus.objects.get(date=max_date)
		except:
			last_status = 'no status'
		return last_status


	def get_last_error(self):

		Base().connection()

		try:
			max_date = PubCompareError.objects.all().aggregate(Max('date'))['date__max']
			last_error = PubCompareError.objects.get(date=max_date)
		except:
			last_error = 'no status'
		return last_error

	def save_error(self):

		Base().connection()

		e_type, e_value, e_traceback = sys.exc_info()
		error = PubCompareError.objects.create(
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

		PubCompareStatus.objects.create(
			status = status,
			count = count,
		)

	def __get_pub_without_status_min_date(self, pub_list):
		return pub_list[0].pubdate

	def get_pub_without_status(self):
		pub_list = NormalizePublication.objects.filter(
			status__isnull=True).exclude(
			title_hashes={}).order_by(
			'pubdate')[:self.pub_without_status_length]
		return pub_list

	def __get_unique_publications_min_date(self, pub_without_status_min_date):
		return pub_without_status_min_date-timezone.timedelta(days=self.retrospective_days_delta)

	def __get_unique_publications(self, pub_without_status_min_date):


		min_date_unique = self.__get_unique_publications_min_date(
			pub_without_status_min_date)

		pub_unique = NormalizePublication.objects.filter(
			pubdate__gt=min_date_unique,
			pubdate__lt=pub_without_status_min_date,
			status=PubCompare().status['unique']['db_value']
		).values('id', 'title_hashes', 'text_hashes')

		result = []
		for pub in pub_unique:
			result.append({
				'id': pub['id'],
			 	'title_hashes': pub['title_hashes'],
			 	'text_hashes': pub['text_hashes']
		 	})

		return result

	def start(self):
		# список публикаций без статуса
		publications = Program().get_pub_without_status()

		pub_without_status_min_date = self.__get_pub_without_status_min_date(publications)

		# список уникальных публикаций
		unique_publications = self.__get_unique_publications(pub_without_status_min_date)

		# поиск статуса
		self.__search_status(publications, unique_publications)

		bulk_update(publications)

		self.save_status(len(publications))

	def __search_status(self, publications, unique_publications):
		for publication in publications:
			self.__compare_publication_with_unique_publications(publication, unique_publications)

	def __compare_publication_with_unique_publications(self, publication, unique_publications):

		if len(unique_publications) > 0:
			for unique_publication in unique_publications:
				result = PubCompare().get_status(publication, unique_publication)
				if result['status'] == 'reprint':
					publication.status = PubCompare().status['reprint']['db_value']
					publication.parent_id = unique_publication['id']
					break
				if result['status'] == 'copy':
					publication.status = PubCompare().status['copy']['db_value']
					publication.parent_id = unique_publication['id']
					break
			if publication.status == None:
				publication.status = PubCompare().status['unique']['db_value']
				self.__add_publication_in_unique_publications(publication, unique_publications)
		else:
			publication.status = PubCompare().status['unique']['db_value']
			self.__add_publication_in_unique_publications(publication, unique_publications)

	def __add_publication_in_unique_publications(self, publication, unique_publications):
		unique_publications.append({
			'id':publication.id,
			'title_hashes': publication.title_hashes,
			'text_hashes': publication.text_hashes,
		})

	def clear_statuses(self):
		NormalizePublication.objects.exclude(status__isnull=True).update(status=None)

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