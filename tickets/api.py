from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.TicketList.as_view()),
    url(r'^/types$', views.TicketTypeList.as_view()),
    url(r'^/types/(?P<pk>[0-9]+)$', views.TicketTypeDetail.as_view()),
    url(r'^/(?P<key>[A-z]{1,6}-[0-9]+)$', views.TicketDetail.as_view()),
    url(r'^/(?P<key>[A-z]{1,6}-[0-9]+)/comments$', views.CommentList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
