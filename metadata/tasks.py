from logging import getLogger, Logger

from celery import shared_task
from django.db.models import QuerySet

from metadata.models import Workflow, WorkflowExecution

logger: Logger = getLogger('celery')


@shared_task(bind=True)
def cleanup_workflows(self):
    """
    Remove Workflow related executions so that only 5 latest executions and child objects remain

    :param self: Task
    :return: None
    """
    for workflow in Workflow.objects.all():
        workflow_executions: QuerySet[WorkflowExecution] = WorkflowExecution.objects.filter(workflow=workflow)

        if workflow_executions.count() > 5:
            for workflow_execution in workflow_executions.order_by('-id')[5:]:
                workflow_execution.delete()


@shared_task(bind=True)
def run_workflows(self):
    """
    Run each Workflow

    :param self: Task
    :return: None
    """
    for workflow_id in Workflow.objects.values_list('id', flat=True):
        run_workflow_task.delay(workflow_id=workflow_id)


@shared_task(bind=True)
def run_workflow_task(self, workflow_id: int):
    if not workflow_id:
        raise RuntimeError('`workflow_id` is required!')

    try:
        workflow: Workflow = Workflow.objects.get(pk=workflow_id)
    except Workflow.DoesNotExist:
        raise RuntimeError(f'Workflow: `{workflow_id}` does not exist!')
    else:
        logger.info(f"Running workflow: `{workflow_id}`")

        workflow.run_steps()

        logger.info(f'Finished running workflow: `{workflow_id}`')
