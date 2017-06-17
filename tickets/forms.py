from django import forms

from .models import Attachment

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['attachment']
        widgets = {
            'attachment': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'})
        }
