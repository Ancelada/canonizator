import os
import signal
import json

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .mainapp import MainApp
from .statistics import Statistics
from interface.base import Base
from vocabulary.ajax import VocAjax

def read_ajax(request):
	if request.method == 'POST':
		string = json.loads(request.body)
		response = VocAjax().read_ajax(string, request)
		if response != None:
			return response


def program_statistics_unit(request, program_id):
	if request.user.is_authenticated():
		if any(program_id == program['id'] for program in Statistics().programs):
			args = {}

			#центральная панель
			elems = []

			# статистика программы
			elems.append(render_to_string('program_statistic.html', {
				'program_statistic': Statistics().build_copy_and_normalize_publications_statistics(
					program_id),
			}))

			args['central_panel'] = Base().central_panel(elems)

			#левая панель
			args['left_panel'] = Base().left_panel(Base().build_left_panel_links(
				'program statistics'))

			#правая панель
			args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
			return Base().page(request, args)
		else:
			raise Http404
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def program_statistics(request):
	if request.user.is_authenticated():
		args = {}

		#центральная панель
		elems = []
		elems.append(render_to_string('copy_n_normalize_statistics_list.html', {
			'programs': Statistics().programs,
		}))

		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links(
			'program statistics'))

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))


def pubcompare_statistics(request):
	if request.user.is_authenticated():
		args = {}

		#центральная панель
		elems = []

		# статистика поиска нечетких дублей
		elems.append(render_to_string('statistics_pubcompare.html', {
			'statistics_pubcompare': Statistics().build_statistics_pubcompare(),
		}))

		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links(
			'pubcompare statistics'))

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def common_statistics(request):
	if request.user.is_authenticated():
		args = {}

		#центральная панель
		elems = []

		#общая статистика
		elems.append(render_to_string('statistics_common.html', {
			'statistics_common': Statistics().build_common_statistics(),		
		}))

		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links(
			'common statistics'))

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def vocabulary_statistics(request):
	if request.user.is_authenticated():
		args = {}
		
		#центральная панель
		elems = []
		# статистика словарей
		elems.append(render_to_string('statistics_vocabulary.html', {
			'vocabulary_statistics': Statistics().build_vocabulary_statistics(),			
		}))
		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links('vocabulary statistics'))

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))


def index(request):
	if request.user.is_authenticated():

		template = 'index.html'
		programs = MainApp().start()

		args = {}
		args['programs'] = programs

		#центральная панель
		elems = []
		elems.append(render_to_string(template, args, request=request))
		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links('program manager'))

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def start(request, program_name):
	result = MainApp().run_program(program_name)
	return HttpResponseRedirect(reverse('canonizator:index'))


def stop(request, program_pid):
	if int(program_pid):
		os.kill(int(program_pid), signal.SIGTERM)
	return HttpResponseRedirect(reverse('canonizator:index'))