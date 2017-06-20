from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ExtendedRegistrationForm(UserCreationForm):
    """Extend to include, first_name, last_name, and email."""
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())

    def save(self):
        """Override the save method of UserCreationForm."""
        u = User.objects.create_user(self.data['username'],
                                     self.data['email'],
                                     self.data['password1'],
                                     first_name=self.data['first_name'],
                                     last_name=self.data['last_name'])
        u.save()
