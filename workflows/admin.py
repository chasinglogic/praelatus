from django.contrib import admin

from .models import Workflow, Status, Transition, WebHook


class StatusAdmin(admin.ModelAdmin):
    pass


class WebHookAdmin(admin.StackedInline):
    model = WebHook
    extra = 1


class TransitionInlineAdmin(admin.StackedInline):
    model = Transition
    extra = 0


class TransitionAdmin(admin.ModelAdmin):
    inlines = [
        WebHookAdmin,
    ]


class WorkflowAdmin(admin.ModelAdmin):
    inlines = [
        TransitionInlineAdmin
    ]


admin.site.register(Status, StatusAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(Workflow, WorkflowAdmin)
