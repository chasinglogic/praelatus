from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.WorkflowList.as_view()),
    url(r'^/(?P<pk>[0-9]+)$', views.WorkflowDetail.as_view()),

    url(r'^/transitions$', views.TransitionList.as_view()),
    url(r'^/transitions/(?P<pk>[0-9]+)$', views.TransitionDetail.as_view()),

    url(r'^/statuses$', views.StatusList.as_view()),
    url(r'^/statuses/(?P<pk>[0-9]+)$', views.StatusDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
