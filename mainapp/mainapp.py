import os
import copy
import subprocess
import time

from django.db.models import Max
from .models import *
from . import daemons

class MainApp:

	def __init__(self):
		self.path = os.path.dirname(os.path.abspath(__file__))
		self.program_list = self.__program_list()

	# стартовая страничка канонизатора
	def start(self):
		programs = self.__import_submodules(daemons)
		result = []

		for program in programs:
			# экземпляр класса
			program_unit = programs[program].Program()

			#последний статус
			last_status = program_unit.get_last_status()

			#последняя ошибка
			last_error = program_unit.get_last_error()

			# получаем pid,если имеется
			try:
				pid = program_unit.get_pid()
			except FileNotFoundError:
				pid = 0

			result.append({
				'name': program_unit.name,
				'file_name' : program_unit.file_name,
				'last_status' : last_status,
				'last_error' : last_error,
				'pid': pid
			})
		
		return result

	def run_program(self, program_name):
		programs = self.__import_submodules(daemons)
		program = programs[program_name]

		path = '{0}/daemons/launcher.py'.format(self.path)
		mainapp_dir = os.path.abspath(os.path.join(self.path, os.pardir))
		parent = os.path.abspath(os.path.join(mainapp_dir, os.pardir))

		launcher = open(path, 'r').read()
		basic_content = copy.deepcopy(launcher)
		content = launcher.format(self.path, program_name, program_name)
		launcher = open(path, 'w').write(content)

		subprocess.Popen(['python {0}'.format(path)], shell=True)
		time.sleep(3)
		launcher = open(path, 'w').write(basic_content)


	def __program_list(self):
		programs = self.__import_submodules(daemons)
		program_list = []
		for program in programs:
			program_unit = programs[program].Program()
			program_list.append({'name': program_unit.name})
		return program_list

	def __module_names(self, package):
		for name in os.listdir(os.path.join(self.path, 'daemons')):
			if name.startswith('copy_pub') or name.startswith('normalize_pub') \
			 or name.startswith('links_syn') or name.startswith('make_h') \
			 or name.startswith('pubc') or name.startswith('incorrect'):
				yield name[:-3]

	def __import_submodules(self, package):
		file_names = list(self.__module_names(package))
		m = __import__(package.__name__, globals(), locals(), file_names, 0)
		return dict((name, getattr(m, name)) for name in file_names)