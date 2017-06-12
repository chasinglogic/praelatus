from django.test import TestCase

from .models import Status


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
