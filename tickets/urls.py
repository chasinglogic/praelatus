from django.conf.urls import url

from django_filters.views import FilterView

from . import models, views

urlpatterns = [
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})$', views.show, name='show'),
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})/edit$', views.edit_ticket, name='edit'),
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})/attachment$', views.attachments, name='attachment'),
    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})/link$', views.add_link, name='add_link'),
    url(r'^create/?$', views.create_prompt, name='create_prompt'),
    url(r'^create/(?P<project_key>[A-z-]{1,6})/(?P<ticket_type>[A-z]+)$', views.create, name='create'),
    url(r'^search', views.query),

    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})/transition$', views.transition, name='transition'),

    url(r'^(?P<key>[A-z-]{1,6}-[0-9]{1,})/comment$', views.comment, name='comment'),
    url(r'^comments/(?P<id>[0-9]+)', views.edit_comment, name='edit_comment'),

    url(r'^dashboard', views.dashboard),
]
