# Generated by Django 5.0.4 on 2024-04-19 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0005_alter_stepexecution_is_success_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepexecution',
            name='workflow_execution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_executions', to='metadata.workflowexecution'),
        ),
    ]
