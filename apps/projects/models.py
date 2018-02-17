# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase
from guardian.shortcuts import assign_perm


class Project(models.Model):
    """A project is a way to group work."""

    lead = models.ForeignKey(
        User, related_name='projects', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=140, unique=True)
    key = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    watchers = models.ManyToManyField(User)

    icon = models.ImageField(
        upload_to='projects/icons/', blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    repo = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group)

    class Meta:
        permissions = (('admin_project', 'Can admin the project.'),
                       ('view_project',
                        'Can view the project and it\'s tickets.'),
                       ('create_tickets',
                        'Can create tickets within the project.'),
                       ('edit_tickets',
                        'Can edit tickets within the project.'),
                       ('delete_tickets',
                        'Can delete tickets within the project.'),
                       ('add_comments',
                        'Can comment on tickets within the project.'), )

    def __str__(self):
        """Return the project's name."""
        return self.name


class ProjectUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Project, on_delete=models.CASCADE)


@receiver(post_save, sender=Project)
def create_project_groups(sender, instance=None, created=False, **kwargs):
    if created:
        admin_group = Group(name=instance.name + ' Admin')
        member_group = Group(name=instance.name + ' Contributor')
        user_group = Group(name=instance.name + ' User')
        admin_group.save()
        member_group.save()
        user_group.save()

        assign_perm('admin_project', admin_group, instance)
        assign_perm('create_tickets', admin_group, instance)
        assign_perm('edit_tickets', admin_group, instance)
        assign_perm('delete_tickets', admin_group, instance)
        assign_perm('view_project', admin_group, instance)
        assign_perm('add_comments', admin_group, instance)

        assign_perm('create_tickets', member_group, instance)
        assign_perm('edit_tickets', member_group, instance)
        assign_perm('view_project', member_group, instance)
        assign_perm('add_comments', member_group, instance)

        assign_perm('create_tickets', user_group, instance)
        assign_perm('view_project', user_group, instance)
        assign_perm('add_comments', user_group, instance)

        try:
            anon = User.objects.get(username=getattr(
                settings, 'ANONYMOUS_USER_NAME', 'AnonymousUser'))
            assign_perm('view_project', anon, instance)
        except Exception as e:
            print(e)
            pass

        instance.groups.add(admin_group)
        instance.groups.add(member_group)
        instance.groups.add(user_group)

        instance.watchers.add(instance.lead)

        instance.lead.groups.add(admin_group)
        instance.lead.save()
