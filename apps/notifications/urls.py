from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/acknowledge', views.acknowledge,
        name='acknowledge')
]
