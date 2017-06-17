# from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import WebHook


class InlineWebHookAdmin(GenericStackedInline):
    model = WebHook
    extra = 0
