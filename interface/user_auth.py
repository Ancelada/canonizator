from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.template.loader import render_to_string

from .base import Base

class UserAuth():

	def login(self, request, url):
		
		args = {}

		args['logged_in'] = False

		if request.method == 'POST':
			password = request.POST.get('password', '')
			login = request.POST.get('login', '')
			user = auth.authenticate(username=login, password=password)

			if user is not None:
				auth.login(request, user)
				args['logged_in'] = True

			else:
				args['login_error'] = """
				Пользователь не найден или
				 некорректный пароль
				"""


		args['url'] = url

		# левая панель
		elems = []
		elems.append(render_to_string('textline.html', {'text': 'форма авторизации'}))
		args['left_panel'] = Base().left_panel(elems)
		
		# центральная панель
		elems = []
		elems.append(render_to_string('registration/login.html', args, request=request))
		args['central_panel'] = Base().central_panel(elems)

		# правая панель
		elems = []
		elems.append(render_to_string('textline.html', \
		 {'text': 'Пользователь:{0}'.format(auth.get_user(request).username) }))
		elems.append(render_to_string('link.html', {'url': '/{0}logout/'.format(url), 'text': 'выйти'}))
		args['right_panel'] = Base().right_panel(elems)
		return args

	def logout(self, request, url):
		auth.logout(request)