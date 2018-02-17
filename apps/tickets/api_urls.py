from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import api

urlpatterns = [
    url(r'^$', api.TicketList.as_view()),
    url(r'^/ticketTypes/?$', api.TicketTypeList.as_view()),
    url(r'^/ticketTypes/(?P<pk>[0-9]+)$', api.TicketTypeDetail.as_view()),
    url(r'^/(?P<key>[A-z]{1,6}-[0-9]+)$', api.TicketDetail.as_view()),
    url(r'^/(?P<key>[A-z]{1,6}-[0-9]+)/comments$',
        api.CommentList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
