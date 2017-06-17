from django.contrib import admin

from .models import FieldScheme, WorkflowScheme, TicketType


class FieldSchemeAdmin(admin.ModelAdmin):
    empty_value_display = 'Default'


class WorkflowSchemeAdmin(admin.ModelAdmin):
    empty_value_display = 'Default'


class TicketTypeSchemeAdmin(admin.ModelAdmin):
    empty_value_display = 'Default'


admin.site.register(FieldScheme, FieldSchemeAdmin)
admin.site.register(WorkflowScheme, WorkflowSchemeAdmin)
admin.site.register(TicketType, TicketTypeSchemeAdmin)
