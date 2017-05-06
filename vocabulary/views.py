from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth.models import User

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
		elems.append(Voc().build_table(VocabularyBase().grammems, request.user.id))
		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links('grammems'))

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
			args['left_panel'] = Base().left_panel(Base().build_left_panel_links('grammem'))

			#правая панель
			args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
			return Base().page(request, args)
		else:
			raise Http404
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def tonestatistics(request):
	if request.user.is_authenticated():
		args = {}

		#центральная панель
		elems = []
		# тональность по пользователям
		elems.append(render_to_string('tonestatistics.html', {
			'statistics': Voc().build_tone_statistics(VocabularyBase().grammems)
		}))
		# общая тональность
		elems.append(render_to_string('tonestatistics_common.html', {
			'statistics': Voc().build_tone_statistics_common(VocabularyBase().grammems)
		}))
		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links('tone statistics'))

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def user_select(request):
	if request.user.is_authenticated():
		args = {}

		#центральная панель
		elems = []

		# таблица пользователей
		elems.append(render_to_string('user_select.html', Voc().build_user_select_table(
			User.objects.all(),
			VocabularyBase().grammems,
		)))
		args['central_panel'] = Base().central_panel(elems)

		#левая панель
		args['left_panel'] = Base().left_panel(Base().build_left_panel_links('user select'))

		#правая панель
		args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
		return Base().page(request, args)
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def user_grammems(request, user_id):
	if request.user.is_authenticated():
		if any(user.id==int(user_id) for user in User.objects.all()):
			args = {}
			#центральная панель
			elems = []
			# граммемы пользователя
			elems.append(render_to_string('user_grammems.html', Voc().build_user_grammems(
				user_id,
				VocabularyBase().grammems,
			)))
			args['central_panel'] = Base().central_panel(elems)

			#левая панель
			args['left_panel'] = Base().left_panel(Base().build_left_panel_links('user grammems'))

			#правая панель
			args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
			return Base().page(request, args)
		else:
			raise Http404
	else:
		return redirect('/{0}/login/'.format('canonizator'))

def user_grammem(request, user_id, grammem, page):
	if request.user.is_authenticated():
		if any(user.id==int(user_id) for user in User.objects.all()):
			args = {}
			#центральная панель
			elems = []
			# граммема пользователя
			elems.append(render_to_string('user_grammem.html', Voc().build_user_grammem(
				user_id,
				grammem,
				VocabularyBase().grammems,
				page,
			)))
			args['central_panel'] = Base().central_panel(elems)

			#левая панель
			args['left_panel'] = Base().left_panel(Base().build_left_panel_links('user grammems'))

			#правая панель
			args['right_panel'] = Base().right_panel(Base().build_right_panel_elems(request))
			return Base().page(request, args)
		else:
			raise Http404
	else:
		return redirect('/{0}/login/'.format('canonizator'))