from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase
from guardian.shortcuts import assign_perm


class Project(models.Model):
    """A project is a way to group work."""

    lead = models.ForeignKey(User)
    name = models.CharField(max_length=140, unique=True)
    key = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    icon = models.ImageField(upload_to='projects/icons/', blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    repo = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('admin_project', 'Ability to admin the project.'),
            ('view_project', 'Ability to view the project and it\'s content.'),
            ('create_content', 'Ability to create content within the project.'),
            ('edit_content', 'Ability to edit content within the project.'),
            ('delete_content', 'Ability to delete content within the project.'),
            ('comment_content', 'Ability to comment on content within the project.'),
        )

    def __str__(self):
        """Return the project's name."""
        return self.name


class ProjectUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Project, on_delete=models.CASCADE)


@receiver(post_save, sender=Project)
def create_project_groups(sender, instance=None, **kwargs):
    admin_group = Group(name=instance.name + ' Admin')
    member_group = Group(name=instance.name + ' Member')
    user_group = Group(name=instance.name + ' User')
    admin_group.save()
    member_group.save()
    user_group.save()

    assign_perm('admin_project', admin_group, instance)
    assign_perm('create_content', admin_group, instance)
    assign_perm('edit_content', admin_group, instance)
    assign_perm('delete_content', admin_group, instance)
    assign_perm('view_project', admin_group, instance)
    assign_perm('comment_content', admin_group, instance)

    assign_perm('create_content', member_group, instance)
    assign_perm('edit_content', member_group, instance)
    assign_perm('view_project', member_group, instance)
    assign_perm('comment_content', member_group, instance)

    assign_perm('create_content', user_group, instance)
    assign_perm('view_project', user_group, instance)
    assign_perm('comment_content', user_group, instance)

    try:
        anon = User.objects.get(
            username=getattr(settings,
                             'ANONYMOUS_USER_NAME',
                             'AnonymousUser'))
        assign_perm('view_project', anon, instance)
    except Exception as e:
        print(e)
        pass

    instance.lead.groups.add(admin_group)
    instance.lead.save()
