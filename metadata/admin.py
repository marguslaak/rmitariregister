from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html

from metadata.models import Workflow, StepDefinition, StepExecution, WorkflowExecution
from metadata.tasks import run_workflow_task


class StepExecutionInline(admin.TabularInline):
    model = StepDefinition
    extra = 0


@admin.register(Workflow)
class StepsWorkflowAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    actions = ['run_workflows']
    inlines = [StepExecutionInline]

    @admin.action(description="Run selected workflows")
    def run_workflows(self, request: WSGIRequest, queryset: QuerySet[Workflow]):
        for workflow in queryset:
            run_workflow_task.delay(workflow_id=workflow.pk)


class StepExecutionInline(admin.TabularInline):
    model = StepExecution
    extra = 0
    readonly_fields = [
        'step_definition',
        'status',
        'start_time',
        'end_time',
        'metadata',
        'download_link',
        'is_success',
        'errors'
    ]
    exclude = ['file_path']
    can_delete = False

    def download_link(self, obj: StepExecution) -> str:
        if obj.id and obj.file_path:
            url = reverse('download_parquet_file', args=[str(obj.id)])
            return format_html('<a href="{}">Download</a>', url)
        return 'No Attachment'

    download_link.short_description = "File"


@admin.register(WorkflowExecution)
class StepExecutionAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'status', 'start_time', 'end_time', 'is_success']
    search_fields = ['step_definition', 'status', 'is_success', 'errors']
    list_filter = ['status', 'is_success']
    readonly_fields = ['workflow', 'status', 'start_time', 'end_time', 'is_success', 'errors']
    inlines = [StepExecutionInline]
