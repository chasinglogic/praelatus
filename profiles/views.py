from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated():
        return redirect('/tickets/dashboard')
    form = UserCreationForm()
    return render(request, 'index.html', {'form': form})


def register(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/tickets/dashboard')
    return render(request, 'registration/register.html', {'form': form})


def show(request, username=''):
    u = User.objects.get(username=username)
    return render(request, 'users/show.html', {'profile_user': u})
