from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Project
        help_texts = {
            'key': ("WARNING: Changing this field will break links to this "
                    "project and it's tickets. This will also update all "
                    "tickets in this project to have the new project key.")
        }

        fields = [
            'key', 'name', 'lead', 'description', 'icon', 'homepage', 'repo'
        ]
