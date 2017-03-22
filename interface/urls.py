from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^(?P<url>.+)login/$', views.login, name='login'),
	url(r'^(?P<url>.+)logout/$', views.logout, name='logout'),
]