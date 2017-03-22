import os
import signal

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from .mainapp import MainApp
from interface.base import Base

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