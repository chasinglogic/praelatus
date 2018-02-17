from django.contrib import admin

from .models import Label


class LabelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Label, LabelAdmin)
