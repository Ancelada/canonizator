from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^canonizator/$', views.index, name='index'),

    url(r'^canonizator/program/start/(?P<program_name>[a-zA-Z_]+)$',
        views.start, name='start'),

    url(r'^canonizator/program/stop/(?P<program_pid>[0-9]+)/$',
        views.stop, name='stop'),

    url(r'^program_statistics/$', views.program_statistics),

    url(r'^program_statistics/(?P<program_id>.*)/$', views.program_statistics_unit),

    url(r'^pubcompare_statistics/$', views.pubcompare_statistics),

    url(r'^vocabulary_statistics/$', views.vocabulary_statistics),

    url(r'^common_statistics/$', views.common_statistics),

    url(r'^ajax/$', views.read_ajax, name='ajax'),
]