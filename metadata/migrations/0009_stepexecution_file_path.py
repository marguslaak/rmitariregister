# Generated by Django 5.0.4 on 2024-04-25 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_merge_20240424_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepexecution',
            name='file_path',
            field=models.CharField(blank=True, null=True),
        ),
    ]