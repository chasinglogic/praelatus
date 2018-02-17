from django.contrib.auth.models import User
from django.test import TestCase

from fields.models import Field
from projects.models import Project
from workflows.models import Status, Workflow

from .models import FieldScheme, FieldSchemeField, TicketType, WorkflowScheme


class TestSchemes(TestCase):
    def setUp(self):
        fone = Field(name='Test Field One', data_type='INTEGER')
        fone.save()
        ftwo = Field(name='Test Field Two', data_type='INTEGER')
        ftwo.save()

        s = Status(name='Blah')
        s.save()

        wone = Workflow(name='Test Flow One', create_status=s)
        wone.save()
        wtwo = Workflow(name='Test Flow Two', create_status=s)
        wtwo.save()

        u = User.objects.create_user('fakelead', 'fake@fa.ke', 'fake')
        u.save()

        self.project = Project(
            key='SCHEME', name='Test Scheme Project', lead=u)
        self.project.save()

        self.ttypeone = TicketType(name='Test Type One')
        self.ttypeone.save()
        self.ttypetwo = TicketType(name='Test Type One')
        self.ttypetwo.save()

        self.default_wkflow_scheme = WorkflowScheme(
            workflow=wone, project=self.project)
        self.default_wkflow_scheme.save()

        self.ttypeone_wkflow_scheme = WorkflowScheme(
            workflow=wtwo, project=self.project, ticket_type=self.ttypeone)
        self.ttypeone_wkflow_scheme.save()

        self.default_field_scheme = FieldScheme(
            name='Default Field Scheme', project=self.project)
        self.default_field_scheme.save()

        FieldSchemeField(field=fone, scheme=self.default_field_scheme).save()

        self.ttypeone_field_scheme = FieldScheme(
            name='Ttypeone Field Scheme',
            project=self.project,
            ticket_type=self.ttypeone)
        self.ttypeone_field_scheme.save()

        FieldSchemeField(field=fone, scheme=self.ttypeone_field_scheme).save()
        FieldSchemeField(field=ftwo, scheme=self.ttypeone_field_scheme).save()

    def test_workflow_scheme_get(self):
        default = WorkflowScheme.get_for_project(project=self.project)
        self.assertEqual(default, self.default_wkflow_scheme)

        default = WorkflowScheme.get_for_project(
            project=self.project, ticket_type=self.ttypetwo)
        self.assertEqual(default, self.default_wkflow_scheme)

        not_default = WorkflowScheme.get_for_project(
            project=self.project, ticket_type=self.ttypeone)
        self.assertEqual(not_default, self.ttypeone_wkflow_scheme)

    def test_field_scheme_get(self):
        default = FieldScheme.get_for_project(project=self.project)
        self.assertEqual(default, self.default_field_scheme)

        self.assertEqual(len(default.fields.all()), 1)

        default = FieldScheme.get_for_project(
            project=self.project, ticket_type=self.ttypetwo)
        self.assertEqual(default, self.default_field_scheme)

        not_default = FieldScheme.get_for_project(
            project=self.project, ticket_type=self.ttypeone)
        self.assertEqual(not_default, self.ttypeone_field_scheme)
        self.assertEqual(len(not_default.fields.all()), 2)
