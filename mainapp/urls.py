from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^canonizator/$', views.index, name='index'),
    url(r'^canonizator/program/start/(?P<program_name>[a-zA-Z_]+)$',
        views.start, name='start'),
    url(r'^canonizator/program/stop/(?P<program_pid>[0-9]+)/$',
        views.stop, name='stop'),
    url(r'^statistics/$', views.statistics, name='statistics'),
]