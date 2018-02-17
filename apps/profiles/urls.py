# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/$', views.index, name='index'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^(?P<username>[A-z0-9]+)$', views.show, name='show'),
]
