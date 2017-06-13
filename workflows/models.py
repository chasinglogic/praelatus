import enum
from django.db import models


class Workflow(models.Model):
    """A workflow is a set of statuses and transitions."""
    name = models.CharField(max_length=255)
    description = models.TextField()


class State(enum.Enum):
    """Indicates whether a Status is ToDo, In Progress, or Done."""
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


class Status(models.Model):
    """A state in the process of a workflow."""
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=11, default=State.TODO.value)
    # Hex color for the background of the Status Pill
    bg_color = models.CharField(max_length=7)

    @property
    def is_todo(self):
        """Indicate if this is a waiting to be worked status."""
        return self.state == State.TODO.value

    @property
    def is_in_progress(self):
        """Indicate if this is a being worked status."""
        return self.state == State.IN_PROGRESS.value

    @property
    def is_done(self):
        """Indicate if this is a completed status."""
        return self.state == State.DONE.value


class Transition(models.Model):
    """A transition from one status to another."""
    name = models.CharField(max_length=255, default='Create')
    workflow = models.ForeignKey(Workflow, related_name='transitions')
    to_status = models.ForeignKey(Status, related_name='+')
    from_status = models.ForeignKey(Status, related_name='+', null=True)


class WebHook(models.Model):
    """A web hook is ran when the associated transition is executed."""
    name = models.CharField(max_length=255)
    url = models.TextField()
    method = models.CharField(max_length=10)
    body = models.TextField()
    transition = models.ForeignKeyField(Transition, related_name='web_hooks')
