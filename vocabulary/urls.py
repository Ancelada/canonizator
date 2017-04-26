from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^vocabulary/grammems/$', views.grammems, name='grammems'),
    url(r'^vocabulary/grammems/(?P<grammem>[a-zA-Z_]+)/$', views.grammem, name='grammem'),
]