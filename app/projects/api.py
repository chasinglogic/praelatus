from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.ProjectList.as_view()),
    url(r'^/(?P<key>[A-z]{1,6})$', views.ProjectDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
