from django.shortcuts import redirect

from .user_auth import UserAuth
from .base import Base

def login(request, url=None):
	args = UserAuth().login(request, url)
	if args['logged_in'] == True:
		return redirect('/{0}'.format(url))
	return Base().page(request, args)

def logout(request, url=None):
	args = UserAuth().logout(request, url)
	if url != None:
		return redirect('/{0}'.format(url))
	else:
		return redirect('/')