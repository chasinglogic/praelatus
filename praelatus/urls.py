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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Django builtins
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^admin/', admin.site.urls),

    # App Routes
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^tickets/', include('tickets.urls', namespace='tickets')),

    # API Routes
    url(r'^api/auth/', include('rest_framework.urls', namespace='drf')),
    url(r'^api/tickets', include('tickets.api', namespace='tickets_api')),
    url(r'^api/projects', include('projects.api', namespace='projects_api')),
    url(r'^api/fields', include('fields.api', namespace='fields_api')),
    url(r'^api/labels', include('labels.urls', namespace='labels_api')),
    url(r'^api/workflows', include('workflows.api', namespace='workflows_api')),
]
