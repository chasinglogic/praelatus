from django.contrib import admin
from .models import Field, FieldOption


class FieldAdmin(admin.ModelAdmin):
    filter_horizontal = ('options',)

    class Media:
        js = ('/static/fields/js/admin.js',)


admin.site.register(FieldOption)
admin.site.register(Field, FieldAdmin)
