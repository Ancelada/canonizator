from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib import auth

class Base:

	def left_panel(self, elems):
		return render_to_string('left_panel.html', {'elems': elems})

	def central_panel(self, elems):
		return render_to_string('central_panel.html', {'elems': elems})

	def right_panel(self, elems):
		return render_to_string('right_panel.html', {'elems' : elems})

	def page(self, request, args):
		return render(request, 'page.html', args)

	def username(self, request):
		return auth.get_user(request).username