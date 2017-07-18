from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestProfileCreation(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user('testprofile', 'test@example.com',
                                        'test')
        user.save()
        self.assertTrue(user.profile is not None)
        self.assertTrue(user.profile.gravatar is not None)
        self.assertTrue(user.profile.profile_pic is not None)
        self.assertTrue(user.profile.profile_pic == user.profile.gravatar)

    def test_profile_update(self):
        user = User.objects.create_user('testupdate', 'test@example.com',
                                        'test')
        user.save()
        orig = user.profile.gravatar
        user.email = 'blank@blank.com'
        user.save()
        self.assertTrue(user.profile.gravatar != orig)


class TestViews(TestCase):
    def test_index_anon(self):
        res = self.client.get(reverse('index'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'index.html')

    def test_index_auth(self):
        user = User.objects.create_user('testuser', 'test@example.com', 'test')
        user.save()
        self.client.login(username='testuser', password='test')
        res = self.client.get(reverse('index'), follow=True)
        self.assertRedirects(res, settings.LOGIN_REDIRECT_URL)

    def test_registration(self):
        test_user = {
            'username': 'testregister',
            'password1': 'bananapeel123',
            'password2': 'bananapeel123',
            'email': 'test@email.com',
            'first_name': 'Test',
            'last_name': 'Testerson'
        }

        res = self.client.post(reverse('users:register'), test_user)
        self.assertRedirects(res, settings.LOGIN_REDIRECT_URL)
        u = User.objects.get(username='testregister')
        self.assertTrue(u.email == test_user['email'])
        self.assertTrue(u.first_name == test_user['first_name'])
        self.assertTrue(u.last_name == test_user['last_name'])
        self.assertTrue(u.check_password('bananapeel123'))
