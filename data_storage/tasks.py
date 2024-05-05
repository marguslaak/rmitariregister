from logging import getLogger, Logger

from celery import shared_task


logger: Logger = getLogger('celery')


@shared_task(bind=True)
def task_1(self):
    logger.info('Running Task 1...')
