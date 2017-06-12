from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search', views.search, name='search'),
    url(r'^(?P<key>[A-z0-9]{1,6})$', views.show, name='show'),
]
