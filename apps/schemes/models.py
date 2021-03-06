# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

from django.db import models

from fields.models import Field
from projects.models import Project
from tickets.models import TicketType
from workflows.models import Workflow


class FieldScheme(models.Model):
    """Determine what fields a project wants for a ticket type."""
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='field_schemes', on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(
        TicketType, related_name='field_schemes', blank=True, null=True, on_delete=models.PROTECT)

    @classmethod
    def get_for_project(cls, project=None, ticket_type=None, **kwargs):
        schemes = cls.objects.filter(project=project,
                                     ticket_type=ticket_type)
        if len(schemes) == 0:
            schemes = cls.objects.filter(project=project,
                                         ticket_type=None)

        if len(schemes) > 0:
            return schemes[0]
        return None

    class Meta:
        unique_together = ('project', 'ticket_type', )

    def __str__(self):
        """Return the scheme's name."""
        return '%s for %s' % (self.name, self.project.name)


class FieldSchemeField(models.Model):
    """A field on a FieldScheme"""
    required = models.BooleanField(default=False)
    scheme = models.ForeignKey(FieldScheme, related_name='fields', on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('scheme', 'field', )

    @property
    def name(self):
        return self.field.name

    @property
    def options(self):
        return self.field.options

    @property
    def data_type(self):
        return self.field.data_type


class WorkflowScheme(models.Model):
    """Tie a workflow to a project for a TicketType."""
    project = models.ForeignKey(Project, related_name='workflow_schemes', on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, related_name='schemes', on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(
        TicketType, related_name='workflow_schemes', null=True, blank=True, on_delete=models.PROTECT)

    @classmethod
    def get_for_project(cls, project=None, **kwargs):
        schemes = cls.objects.filter(project=project, **kwargs)

        if len(schemes) == 0:
            schemes = cls.objects.filter(project=project, ticket_type=None)

        if len(schemes) > 0:
            return schemes[0]
        return None

    class Meta:
        unique_together = ('project', 'ticket_type', 'workflow', )
