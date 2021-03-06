from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Status, Transition, WebHook, Workflow


class InlineWebHookAdmin(GenericStackedInline):
    model = WebHook
    extra = 0


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
