from django.conf.urls import url
from django_filters.views import FilterView

from . import views
from . import models

urlpatterns = [
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})$', views.show, name='show'),
    url(r'^search', FilterView.as_view(model=models.Ticket)),
]
