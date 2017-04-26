from django.http import Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import redirect

from interface.base import Base
from .base import Base as VocabularyBase
from .vocabulary import Voc
# Create your views here.
def grammems(request):
	if request.user.is_authenticated():
		
		args = {}

		#центральная панель
		elems = []

		# статистика поиска нечетких дублей
		elems.append(Voc().build_table(VocabularyBase().grammems))
		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		elems = []
		elems.append(render_to_string('link.html', {
			'url': '/canonizator/', 'text': 'program manager'}))
		elems.append(render_to_string('link.html', {
		 'url': '/statistics/', 'text': 'program statistics'}))
		elems.append(render_to_string('textline.html', {'text': 'grammems'}))
		args['left_panel'] = Base().left_panel(elems)

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))

		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def grammem(request, grammem):
	if request.user.is_authenticated():
		if any(grm['url'] == grammem for grm in VocabularyBase().grammems):
			args = {}

			#центральная панель
			elems = []

			# слова граммемы
			elems.append(Voc().build_grammem_page(grammem, VocabularyBase().grammems))
			args['central_panel'] = Base().central_panel(elems)

			#левая панель
			elems = []
			elems.append(render_to_string('link.html', {
				'url': '/canonizator/', 'text': 'program manager'}))
			elems.append(render_to_string('link.html', {
			 'url': '/statistics/', 'text': 'program statistics'}))
			elems.append(render_to_string('link.html', {
				'url': '/vocabulary/grammems/', 'text': 'grammems'}))
			elems.append(render_to_string('textline.html', {
				'text': grammem,	
			}))

			elems.append(render_to_string('textline.html', {'text': 'grammems'}))
			args['left_panel'] = Base().left_panel(elems)

			#правая панель
			args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
			return Base().page(request, args)
		else:
			raise Http404
	else:
		return redirect('/{0}/login/'.format('canonizator'))