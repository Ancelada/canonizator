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

from mainapp.models import *
from django.db.models import Max
from manager.models import Publication
from mainapp.daemons.base import Base


class Program:

	def __init__(self):
		self.name = 'Копирование'
		self.file_name = 'copy_publications'
		self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.pids_dir = os.path.join(self.base_dir, 'daemons/pids')
		self.statuses_dir = os.path.join(self.base_dir, 'daemons/statuses')
		self.context = Base().create_daemon_context(self.file_name)

	def get_last_status(self):
		try:
			max_date = CopyPublicationStatus.objects.all().aggregate(Max('date'))['date__max']
			last_status = CopyPublicationStatus.objects.get(date=max_date)
		except:
			last_status = 'no status'
		return last_status

	def get_last_error(self):
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

	def push(self, date):

		Base().connection()

		if date == None:
			publications = Publication.objects.using('manager').all().values('title', 'text', 'date', \
				 'crawler__name', 'author')[:3000]
		else:
			publications = Publication.objects.using('manager').filter( \
				date__gte=date).values('title', \
			 'text', 'date', 'crawler__name', 'author')[:3000]

		publications_filtered = []

		# убираем дубли, если они существуют в manager.Publication
		for publication in publications:
			doubled = 0
			for publication_filtered in publications_filtered:
				if publication['title'] == publication_filtered['title'] and \
				publication['text'] == publication_filtered['text'] and \
				publication['date'] == publication_filtered['date'] and \
				publication['crawler__name'] == publication_filtered['crawler__name'] and \
				publication['author'] == publication_filtered['author']:
					doubled = 1
			if doubled == 0:
				publications_filtered.append(publication)

		# убираем дубли, если они существуют в canonizator.PublicationCopy
		publication_copys = CopyPublication.objects.filter(date__gte=date).values('title', 'text', \
			'date', 'name', 'author')

		for publication_copy in publication_copys:
			for publication_filtered in publications_filtered:
				if publication_filtered['title'] == publication_copy['title'] and \
				publication_filtered['text'] == publication_copy['text'] and \
				publication_filtered['date'] == publication_copy['date'] and \
				publication_filtered['crawler__name'] == publication_copy['name'] and \
				publication_filtered['author'] == publication_copy['author']:
					publications_filtered.remove(publication_filtered)

		# записываем в CopyPublication publications_filtered
		publication_copys = []
		for publication_filtered in publications_filtered:
			publication_copys.append(CopyPublication(name=publication_filtered['crawler__name'], \
				title=publication_filtered['title'], text=publication_filtered['text'], \
				 date=publication_filtered['date'], author=publication_filtered['author']))

		count = len(publication_copys)
		if count > 0:
			CopyPublication.objects.bulk_create(publication_copys)

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