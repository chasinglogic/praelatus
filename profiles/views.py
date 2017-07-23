from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import generics, filters

from .forms import ExtendedRegistrationForm
from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    """API for Users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', 'email')


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


def index(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    form = ExtendedRegistrationForm()
    return render(request, 'index.html', {'form': form})


def register(request):
    form = ExtendedRegistrationForm()
    if request.method == 'POST':
        form = ExtendedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'registration/register.html', {'form': form})


def show(request, username=''):
    u = User.objects.get(username=username)
    return render(request, 'users/show.html', {'profile_user': u})
