# Generated by Django 5.0.4 on 2024-04-18 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_rename_has_errors_stepexecution_is_success_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepexecution',
            name='is_success',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workflowexecution',
            name='is_success',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
