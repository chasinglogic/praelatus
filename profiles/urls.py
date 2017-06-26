from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/$', views.index, name='index'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^(?P<username>[A-z0-9]+)$', views.show, name='show'),
]
