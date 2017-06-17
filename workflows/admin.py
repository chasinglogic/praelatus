from django.contrib import admin
from .models import Workflow, Status, Transition
from hooks.admin import InlineWebHookAdmin


class StatusAdmin(admin.ModelAdmin):
    pass


class TransitionInlineAdmin(admin.StackedInline):
    model = Transition
    extra = 0


class TransitionAdmin(admin.ModelAdmin):
    inlines = [
        InlineWebHookAdmin,
    ]


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [
        TransitionInlineAdmin,
        InlineWebHookAdmin
    ]


admin.site.register(Status, StatusAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(Workflow, WorkflowAdmin)
