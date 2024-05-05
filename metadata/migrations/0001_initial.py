# Generated by Django 5.0.4 on 2024-04-18 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StepDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('sql_query', models.TextField()),
                ('result_filename', models.CharField(max_length=100)),
                ('validation_schema', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StepExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('has_errors', models.BooleanField()),
                ('errors', models.JSONField()),
                ('step_definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.stepdefinition')),
            ],
        ),
        migrations.AddField(
            model_name='stepdefinition',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.workflow'),
        ),
    ]
