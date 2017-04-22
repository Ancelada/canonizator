import os
import sys
import traceback
import psutil
import time
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'canonizator'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'canonizator.settings'

from django.conf import settings
import django
django.setup()

from mainapp.models import *
from django.db.models import Max
from manager.models import Publication
from mainapp.daemons.base import Base


class Program:

	def __init__(self):
		self.publications_count = 10
		self.name = 'Копирование'
		self.file_name = 'copy_publications'
		self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
		self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')
		self.context = Base().create_daemon_context(self.file_name)

		self.publication_table_columns = [
			'crawler__id',
			'crawler__name',
			'crawler__name_cyrillic',
			'title',
			'text',
			'date',
			'author',
		]

		self.copypublication_table_columns = [
			'crawler_id',
			'title',
			'text',
			'date',
		]

	def get_last_status(self):

		Base().connection()

		try:
			max_date = CopyPublicationStatus.objects.all().aggregate(Max('date'))['date__max']
			last_status = CopyPublicationStatus.objects.get(date=max_date)
		except:
			last_status = 'no status'
		return last_status

	def get_last_error(self):

		Base().connection()

		try:
			max_date = CopyPublicationError.objects.all().aggregate(Max('date'))['date__max']
			last_error = CopyPublicationError.objects.get(date=max_date)
		except:
			last_error = 'no status'
		return last_error

	def save_error(self):

		Base().connection()
		
		e_type, e_value, e_traceback = sys.exc_info()
		error = CopyPublicationError.objects.create(
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

		CopyPublicationStatus.objects.create(
				status = status,
				count = count
			)

	def get_date(self):

		Base().connection()

		try:
			date = CopyPublication.objects.all().aggregate( \
				Max('date'))['date__max']
		except:
			date = None
		return date

	def __remove_doubles(self, publications):
		for key, publication in enumerate(publications):
			if any(p['title'] == publication['title'] and p['text'] == publication['text'] and \
				p['date'] == publication['date'] and p['crawler__id'] == publication['crawler__id'] \
				for p in publications[key+1:]):

				del publications[key]

				return self.__remove_doubles(publications)

		return publications

	def __remove_doubles_by_copypublication_table(self, publications, copypublications):
		for key, publication in enumerate(publications):
			if any(p['crawler_id'] == publication['crawler__id'] and p['title']==publication['title'] \
			 and p['text'] == publication['text'] and p['date'] == publication['date'] \
			  for p in copypublications):

				del publications[key]

				return self.__remove_doubles_by_copypublication_table(publications, copypublications)
		return publications

	def push(self, date):

		Base().connection()

		if date == None:
			publications = list(Publication.objects.using('manager').all().values(
				*self.publication_table_columns
			).order_by('date')[:self.publications_count])
		else:
			publications = list(Publication.objects.using('manager').filter(
				date__gte=date
			).values(
				*self.publication_table_columns
			).order_by('date')[:self.publications_count])


		# убираем дубли, если они существуют в manager.Publication
		publications = self.__remove_doubles(publications)

		# убираем дубли, если они существуют в canonizator.PublicationCopy
		if date != None:

			copypublications = CopyPublication.objects.filter(
				date__gte=date-timedelta(days=1)).values(
					*self.copypublication_table_columns
				)

			publications = self.__remove_doubles_by_copypublication_table(publications, copypublications)

		# записываем в CopyPublication publications_filtered
		copypublications = []

		for publication in publications:
			copypublications.append(CopyPublication(
				crawler_id=publication['crawler__id'],
				name=publication['crawler__name'],
				name_cyrillic=publication['crawler__name_cyrillic'],
				title=publication['title'],
				text=publication['text'],
				date=publication['date'],
				author=publication['author'],
			))

		count = len(copypublications)

		if count > 0:

			Base().connection()

			CopyPublication.objects.bulk_create(copypublications)

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
						date = self.get_date()
						self.push(date)
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