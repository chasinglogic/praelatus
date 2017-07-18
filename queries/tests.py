from django.db.models import Q
from django.test import TestCase

from .dsl import compile_q


class TestQueriesParser(TestCase):
    def test_simple_query(self):
        q = 'summary = "TEST"'
        self.assertEqual(str(compile_q(q)), str(Q(summary__exact='TEST')))

    def test_complex_query(self):
        q = '(summary ~~ "TEST*" and (assignee = "chasinglogic" or reporter = "link867"))'
        self.assertEqual(
            str(compile_q(q)),
            str(
                Q(summary__regex="TEST*") &
                (Q(assignee__username__exact='chasinglogic')
                 | Q(reporter__username__exact='link867'))))

    def test_labels_query(self):
        q = 'labels in ["test", "ops"]'
        self.assertEqual(
            str(compile_q(q)), str(Q(labels__name__in=['test', 'ops'])))
