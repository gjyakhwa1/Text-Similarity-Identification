# Generated by Django 4.0.1 on 2023-03-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bertConnector', '0012_remove_serverstatus_currentquestionspathuse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionAskedDate',
            field=models.DateField(),
        ),
    ]
