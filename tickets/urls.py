from django.conf.urls import url

from django_filters.views import FilterView

from . import models, views

urlpatterns = [
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})$', views.show, name='show'),
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})/transition$', views.transition, name='transition'),
    url(r'^search', FilterView.as_view(model=models.Ticket)),
    url(r'^dashboard', views.dashboard),
]
