# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

"""praelatus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from profiles import views as profile_views

urlpatterns = [
    # Django builtins
    url(r'^logout/?', auth_views.logout, name='logout'),
    url(r'^login/?', auth_views.login, name='login'),
    url(r'^admin/?', admin.site.urls),

    # App Routes
    url(r'^/?$', profile_views.index, name='index'),
    url(r'^projects/?', include(('projects.urls', 'projects'))),
    url(r'^queries/?', include(('queries.urls', 'queries'))),
    url(r'^tickets/?', include(('tickets.urls', 'tickets'))),
    url(r'^notifications/', include(('notifications.urls', 'notifications'))),
    url(r'^users/?', include(('profiles.urls', 'users'))),

    # API Routes
    url(r'^api/auth/?', include('rest_framework.urls')),
    url(r'^api/tickets', include(('tickets.api_urls', 'ticket_api'))),
    url(r'^api/projects', include(('projects.api', 'project_api'))),
    url(r'^api/workflows', include(('workflows.api', 'workflow_api'))),
    url(r'^api/fields', include(('fields.urls', 'fields_api'))),
    url(r'^api/labels', include(('labels.urls', 'labels_api'))),
    url(r'^api/users', include(('profiles.api', 'users_api'))),
]
