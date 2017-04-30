import os
import signal
import json

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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


def statistics(request):
	if request.user.is_authenticated():

		args = {}

		#центральная панель
		elems = []

		# статистика словарей
		elems.append(render_to_string('statistics_vocabulary.html', {
			'vocabulary_statistics': Statistics().build_vocabulary_statistics(),			
		}))

		# статистика по дням
		elems.append(render_to_string('statistics.html', {
			'statistics': Statistics().build_copy_and_normalize_publications_statistics(),
		}))

		#общая статистика
		elems.append(render_to_string('statistics_common.html', {
			'statistics_common': Statistics().build_common_statistics(),		
		}))

		# статистика поиска нечетких дублей
		elems.append(render_to_string('statistics_pubcompare.html', {
			'statistics_pubcompare': Statistics().build_statistics_pubcompare(),
		}))
		
		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		elems = []
		elems.append(render_to_string('link.html', {'url': '/canonizator/', 'text': 'program manager'}))
		elems.append(render_to_string('textline.html', { 'text': 'program statistics'}))
		elems.append(render_to_string('link.html', {'url': '/vocabulary/grammems/', 'text': 'grammems'}))
		elems.append(render_to_string('link.html', {
				'url': '/vocabulary/tonestatistics/', 'text': 'tone statistics'}))
		args['left_panel'] = Base().left_panel(elems)

		#правая панель
		elems = []
		elems.append(render_to_string('textline.html', \
		 {'text': Base().username(request)}))
		elems.append(render_to_string('link.html', { \
			'url': '/{0}/logout/'.format('canonizator'), 'text': 'выйти'}))
		elems.append(render_to_string('link.html', \
		 {'url': '/{0}/login/'.format('canonizator'), 'text': 'войти'}))
		args['right_panel'] = Base().right_panel(elems)
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
		elems = []
		elems.append(render_to_string('textline.html', {'text': 'program manager'}))
		elems.append(render_to_string('link.html', { \
			'url': '/statistics/', 'text': 'program statistics'}))
		elems.append(render_to_string('link.html', {'url': '/vocabulary/grammems/', 'text': 'grammems'}))
		elems.append(render_to_string('link.html', {
				'url': '/vocabulary/tonestatistics/', 'text': 'tone statistics'}))
		args['left_panel'] = Base().left_panel(elems)

		#правая панель
		elems = []
		elems.append(render_to_string('textline.html', \
		 {'text': Base().username(request)}))
		elems.append(render_to_string('link.html', { \
			'url': '/{0}/logout/'.format('canonizator'), 'text': 'выйти'}))
		elems.append(render_to_string('link.html', \
		 {'url': '/{0}/login/'.format('canonizator'), 'text': 'войти'}))
		args['right_panel'] = Base().right_panel(elems)
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