from django.contrib import admin

from hooks.admin import InlineWebHookAdmin

from .models import Status, Transition, Workflow


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
