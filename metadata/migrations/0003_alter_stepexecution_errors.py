# Generated by Django 5.0.4 on 2024-04-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0002_alter_stepdefinition_validation_schema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepexecution',
            name='errors',
            field=models.JSONField(blank=True, null=True),
        ),
    ]