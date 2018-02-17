from django.shortcuts import redirect, render

from .models import Notification


def acknowledge(request, id=0):
    notification = Notification.objects.get(id=id)
    notification.acknowledged = True
    notification.save()
    return redirect('/tickets/dashboard')
