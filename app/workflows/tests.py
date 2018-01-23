from django.test import TestCase

from .models import Status, WebHook


class TestStatusStateHelpers(TestCase):

    def test_is_todo(self):
        s = Status(name='Test Todo', state='TODO')
        self.assertTrue(s.is_todo)

    def test_is_in_progress(self):
        s = Status(name='Test In_Progress', state='IN_PROGRESS')
        self.assertTrue(s.is_in_progress)

    def test_is_done(self):
        s = Status(name='Test Done', state='DONE')
        self.assertTrue(s.is_done)


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
