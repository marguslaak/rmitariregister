import logging
import os
from io import StringIO
from shutil import rmtree
from typing import Optional, Callable
import json

import duckdb
from django.db import models
import pandas as pd
from django.conf import settings
from django.utils import timezone
from pandera import DataFrameSchema
from pandera.errors import SchemaErrors

from metadata.validations import create_dataframe_schema_from_json
from metadata.duckdb_functions import add_duckdb_functions

logger = logging.getLogger(__name__)


class Workflow(models.Model):
    name = models.CharField(max_length=100)

    def run_steps(self):
        workflow_exec = WorkflowExecution(workflow=self, status='running')
        workflow_exec.save()
        workflow_exec.run_workflow()


class StepDefinition(models.Model):
    class Engine(models.TextChoices):
        SQL = 'SQL', 'SQL'
        FUNCTION = 'FUN', 'FUNCTION'
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    order = models.IntegerField()
    sql_query = models.TextField()
    result_filename = models.CharField(max_length=100)
    validation_schema = models.JSONField(blank=True, null=True)
    engine = models.CharField(
        max_length=3,
        choices=Engine.choices,
        default=Engine.SQL
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order} -> {self.result_filename}"


class WorkflowExecution(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    is_success = models.BooleanField(blank=True, null=True)
    errors = models.JSONField(blank=True, null=True)

    @property
    def workdir(self) -> str:
        return os.path.join(settings.BASE_DIR, "workflows", str(self.id))

    def create_folder(self) -> str:
        """
        Create a folder for the workflow execution
        :return:
        """
        if not self.id:
            logger.error("WorkflowExecution object must be saved before creating folder")
            raise ValueError("WorkflowExecution object must be saved before creating folder")

        os.mkdir(self.workdir)

        if os.path.exists(self.workdir):
            return self.workdir

        raise ValueError(f"Could not create folder {self.workdir}")

    def __enter__(self):
        self._currentdir = os.getcwd()
        workdir = self.create_folder()
        os.chdir(workdir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._currentdir)

    def run_workflow(self, continue_flow=False):
        if self.workflow is None:
            raise ValueError("WorkflowExecution must have a workflow to run")

        self.start_time = timezone.now()

        if not continue_flow:
            # We create a new flow
            steps = self.workflow.stepdefinition_set.all().order_by('order')
            for step in steps:
                step_execution = StepExecution(workflow_execution=self, step_definition=step, status='pending')
                step_execution.save()

        with self:
            for idx, step_execution in enumerate(self.step_executions.filter(status__in=['pending', 'failed']).
                                                         order_by('step_definition__order'), start=1):
                logger.info('Running step `%s`', step_execution.step_definition.order)
                step_execution.run()
                if step_execution.status != 'completed':
                    self.status = 'failed'
                    self.is_success = False
                    self.errors = step_execution.errors
                    self.save()
                    return

        self.end_time = pd.Timestamp.now()
        self.status = 'completed'
        self.is_success = True
        self.save()

    def delete(self, using=None, keep_parents=False):
        if os.path.exists(self.workdir):
            rmtree(self.workdir)
        super().delete(using=using, keep_parents=keep_parents)


class StepExecution(models.Model):
    workflow_execution = models.ForeignKey(WorkflowExecution, on_delete=models.CASCADE, related_name='step_executions')
    step_definition = models.ForeignKey(StepDefinition, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    is_success = models.BooleanField(blank=True, null=True)
    errors = models.JSONField(blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    file_path = models.CharField(blank=True, null=True)

    def run(self):
        self.status = 'running'
        self.save(update_fields=['status'])

        start_time = timezone.now()
        warn_only: bool = bool((self.step_definition.validation_schema or {}).pop('warn_only', False))
        validation_schema: DataFrameSchema = create_dataframe_schema_from_json(self.step_definition.validation_schema)

        try:
            data: Optional[pd.DataFrame] = self.get_data()

            if isinstance(data, pd.DataFrame):
                if data.empty:
                    raise Exception('Empty Data Frame!')

                if validation_schema:
                    validation_schema.validate(check_obj=data, lazy=True)
        except Exception as exc:
            if not warn_only:
                logger.exception("Error occurred while running step `%s`", self.step_definition.order)
                self.status = 'failed'
                self.is_success = False
            else:
                logger.warning("Warnings occurred while running step `%s`", self.step_definition.order)

            if isinstance(exc, SchemaErrors):
                schema_errors = {
                    parent_error: {
                        sub_error: [
                            {
                                sub_error_data_key: sub_error_elem[sub_error_data_key]
                                for sub_error_data_key in ['column', 'check', 'error']
                            }
                            for sub_error_elem in sub_error_data
                        ]
                    }
                    for parent_error, parent_error_data in exc.message.items()
                    for sub_error, sub_error_data in parent_error_data.items()
                }

                errors: str = json.dumps(schema_errors)
            else:
                errors: str = str(exc)

            self.errors = errors
            self.save()
            if not warn_only:
                return

        end_time = timezone.now()

        # store result info about the step execution
        self.status = 'completed'
        self.is_success = True
        self.start_time = start_time
        self.end_time = end_time
        self.save()

    def run_python_func(self) -> None:
        """
        Run python function defined in self.step_definition.sql_query

        :return: None, runs python function defined in self.step_definition.sql_query
        """
        import metadata.python_functions as python_functions  # noqa

        step_definition: StepDefinition = self.step_definition

        if not step_definition.sql_query:
            raise RuntimeError('Unable to determine python function!')

        python_func: Optional[Callable] = getattr(
            python_functions,
            step_definition.sql_query.lstrip('_').split('(')[0],
            None
        )

        if not python_func:
            raise RuntimeError('Unknown/invalid python function!')

        try:
            extra_param: str = 'step_execution=self'

            eval(f'python_functions.{step_definition.sql_query[:-1]}, {extra_param})')
        except Exception as exc:
            raise RuntimeError(f'Error occurred while running func: {python_func.__name__}') from exc

    def get_data(self) -> Optional[pd.DataFrame]:
        # get data from somewhere
        connection: duckdb.DuckDBPyConnection = duckdb.connect()

        add_duckdb_functions(connection)

        step_definition: StepDefinition = self.step_definition

        result: Optional[duckdb.DuckDBPyRelation] = None

        if step_definition.engine == StepDefinition.Engine.SQL:
            result: duckdb.DuckDBPyRelation = connection.query(step_definition.sql_query)
            if result:
                count: int = result.count("*").fetchall()[0][0]
            else:
                count = 0

            if (count > 0
                    and step_definition.result_filename
                    and step_definition.result_filename.endswith('.parquet')):
                result.write_parquet(step_definition.result_filename)  # noqa
                self.file_path = os.path.join(self.workflow_execution.workdir, step_definition.result_filename)
                self.save(update_fields=['file_path'])
        elif step_definition.engine == StepDefinition.Engine.FUNCTION:
            self.run_python_func()
        else:
            raise RuntimeError(f"Unsupported engine `{step_definition.engine}`!")

        try:
            df: pd.DataFrame = result.df()

            buffer = StringIO()

            df.info(buf=buffer)

            self.metadata = '\n'.join(buffer.getvalue().split('\n')[1:])
            self.save(update_fields=['metadata'])
        except Exception:  # noqa: broad-except
            df: None = None

        return df
