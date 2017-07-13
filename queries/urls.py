from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/?$', views.index, name='index'),
    url(r'(?P<id>[0-9]+)$', views.query, name='query'),
    url(r'mine/?$', views.mine, name='mine')
]
