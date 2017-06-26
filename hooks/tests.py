from django.test import TestCase

from .models import WebHook


class TestWebHooks(TestCase):

    def test_fire_hook(self):
        hook = WebHook(
            name='Test Web Hook',
            url='{{ url }}{% if uri %}{{ uri }}{% endif %}',
            body='',
            method='GET'
        )

        res = hook.fire_hook({'url': 'https://google.com'})
        self.assertTrue(res.status_code == 200 or res.status_code == 302)
