from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib import auth

class Base:

	def __init__(self):

		self.left_panel_type = {

			'link': 'link.html',
			'textline': 'textline.html',
		}

		self.left_panel_urls = {
			'program manager': {
				'url': '/canonizator/',
				'text': 'program manager',
			},
			'program statistics': {
				'url': '/program_statistics/',
				'text': 'program statistics',
			},
			'common statistics': {
				'url': '/common_statistics/',
				'text': 'common statistics',
			},
			'pubcompare statistics': {
				'url': '/pubcompare_statistics/',
				'text': 'pubcompare statistics'
			},
			'vocabulary statistics': {
				'url': '/vocabulary_statistics/',
				'text': 'vocabulary statistics',
			},
			'grammems': {
				'url': '/vocabulary/grammems/',
				'text': 'grammems',
			},
			'tone statistics': {
				'url': '/vocabulary/tonestatistics/',
				'text': 'tone statistics',
			},
			'user select': {
				'url': '/vocabulary/user_select/',
				'text': 'user select',
			}
		}

	def build_left_panel_links(self, current_line_name):
		result = []

		for key, value in self.left_panel_urls.items():
			if key != current_line_name:
				result.append(
					render_to_string(self.left_panel_type['link'], self.left_panel_urls[key])
				)
			else:
				result.append(
					render_to_string(self.left_panel_type['textline'], {
						'text': self.left_panel_urls[key]['text']})
				)	
		if not current_line_name in self.left_panel_urls:
			result.append(
				render_to_string(self.left_panel_type['textline'], {
					'text': current_line_name})
			)
		return result

	def left_panel(self, elems):
		return render_to_string('left_panel.html', {'elems': elems})

	def central_panel(self, elems):
		return render_to_string('central_panel.html', {'elems': elems})

	def right_panel(self, elems):
		return render_to_string('right_panel.html', {'elems' : elems})


	def build_right_panel_elems(self, request):
		elems = []
		elems.append(render_to_string('textline.html', \
		 {'text': Base().username(request)}))
		elems.append(render_to_string('link.html', { \
			'url': '/{0}/logout/'.format('canonizator'), 'text': 'выйти'}))
		return elems


	def page(self, request, args):
		return render(request, 'page.html', args)

	def username(self, request):
		return auth.get_user(request).username