from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search', views.search, name='search'),
    url(r'^(?P<key>[A-z0-9]{1,6})$', views.show, name='show'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin$', views.admin, name='admin'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/edit$', views.edit, name='edit'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/removePermission$',
        views.remove_permission,
        name='remove_permission'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/addPermission$',
        views.add_permission,
        name='add_permission'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/addTicketType$',
        views.add_ticket_type,
        name='add_ticket_type'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/removeTicketType$',
        views.remove_ticket_type,
        name='remove_ticket_type'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/addWorkflow$',
        views.add_workflow,
        name='add_workflow'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/removeWorkflow$',
        views.remove_workflow,
        name='remove_workflow'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/addUserToGroup$',
        views.add_user_to_group,
        name='add_user_to_group'),
    url(r'^(?P<key>[A-z0-9]{1,6})/admin/removeUserFromGroup$',
        views.remove_user_from_group,
        name='remove_user_from_group'),
]
