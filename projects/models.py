from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """A project is a way to group work."""

    lead = models.ForeignKey(User)
    name = models.CharField(max_length=140)
    key = models.CharField(max_length=10)
    description = models.TextField()

    icon_url = models.CharField(max_length=255)
    homepage = models.CharField(max_length=255)
    repo = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('admin_project', 'Ability to admin the project.'),
            ('view_project', 'Ability to view the project.'),
            ('create_content', 'Ability to create content within the project.'),
            ('edit_content', 'Ability to edit content within the project.'),
            ('comment_content', 'Ability to comment on content within the project.'),
        )

    def __str__(self):
        """Return the project's name."""
        return self.name
