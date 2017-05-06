from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^vocabulary/grammems/$', views.grammems, name='grammems'),
    url(r'^vocabulary/grammems/(?P<grammem>[a-zA-Z_]+)/$', views.grammem, name='grammem'),
    url(r'^vocabulary/tonestatistics/$', views.tonestatistics, name='tonestatistics'),
    url(r'^vocabulary/user_select/$', views.user_select, name='user_select'),
    url(r'^vocabulary/user_grammems/(?P<user_id>\d+)/$', views.user_grammems, name='user_grammems'),
    url(r'^vocabulary/user_grammem/(?P<user_id>\d+)/(?P<grammem>[a-zA-Z_]+)/(?P<page>\d+)/$', views.user_grammem),
]