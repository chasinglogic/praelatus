# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.FieldList.as_view()),
    url(r'^datatypes/$', views.data_types),
    url(r'^(?P<pk>[0-9]+)/$', views.FieldDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
