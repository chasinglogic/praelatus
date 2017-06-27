from django.contrib.auth.models import Group, User
from django.test import TestCase
from guardian.shortcuts import get_perms

from .models import Project


class TestPermissions(TestCase):

    def test_guardian_permissions(self):
        u = User.objects.create_user('testlead', 'test@example.com', 'test')
        u.save()

        p = Project(lead=u, name='Test Project', key='TEST')
        p.save()

        groups = Group.objects.filter(name__startswith=p.name).all()
        self.assertTrue(len(groups) == 3)

        admin = Group.objects.get(name=p.name + ' Admin')
        self.assertTrue('admin_project' in get_perms(admin, p))
        self.assertTrue('view_project' in get_perms(admin, p))
        self.assertTrue('create_content' in get_perms(admin, p))
        self.assertTrue('edit_content' in get_perms(admin, p))
        self.assertTrue('delete_content' in get_perms(admin, p))
        self.assertTrue('comment_content' in get_perms(admin, p))

        member = Group.objects.get(name=p.name + ' Member')
        self.assertTrue('view_project' in get_perms(member, p))
        self.assertTrue('create_content' in get_perms(member, p))
        self.assertTrue('edit_content' in get_perms(member, p))
        self.assertTrue('comment_content' in get_perms(member, p))

        user = Group.objects.get(name=p.name + ' User')
        self.assertTrue('view_project' in get_perms(user, p))
        self.assertTrue('create_content' in get_perms(user, p))
        self.assertTrue('comment_content' in get_perms(user, p))
