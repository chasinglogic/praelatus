from django.conf.urls import url

from django_filters.views import FilterView

from . import views, models

urlpatterns = [
    url(r'^search', FilterView.as_view(model=models.Project), name='search'),
    url(r'^(?P<key>[A-z0-9]{1,6})$', views.show, name='show'),
]
