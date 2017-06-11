from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})$', views.show, name='show'),
]
