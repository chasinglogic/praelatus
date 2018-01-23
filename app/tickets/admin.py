from django.contrib import admin

from .models import TicketType


class TicketTypeSchemeAdmin(admin.ModelAdmin):
    empty_value_display = 'Default'


admin.site.register(TicketType, TicketTypeSchemeAdmin)
