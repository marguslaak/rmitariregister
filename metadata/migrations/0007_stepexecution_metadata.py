# Generated by Django 5.0.4 on 2024-04-22 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_alter_stepexecution_workflow_execution'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepexecution',
            name='metadata',
            field=models.TextField(blank=True, null=True),
        ),
    ]