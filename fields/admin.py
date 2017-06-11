from django.contrib import admin
from .models import Field


class FieldAdmin(admin.ModelAdmin):
    pass


admin.site.register(Field, FieldAdmin)
