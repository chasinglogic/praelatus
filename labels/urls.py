"""URLs for labels, only provides a REST API."""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.LabelList.as_view(), name='list'),
    url(r'^/(?P<pk>[0-9]+)/$', views.LabelDetail.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)