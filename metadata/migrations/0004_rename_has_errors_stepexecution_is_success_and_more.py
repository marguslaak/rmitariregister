# Generated by Django 5.0.4 on 2024-04-18 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0003_alter_stepexecution_errors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stepexecution',
            old_name='has_errors',
            new_name='is_success',
        ),
        migrations.CreateModel(
            name='WorkflowExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('is_success', models.BooleanField()),
                ('errors', models.JSONField(blank=True, null=True)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.workflow')),
            ],
        ),
        migrations.AddField(
            model_name='stepexecution',
            name='workflow_execution',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.workflowexecution'),
            preserve_default=False,
        ),
    ]
