# Generated by Django 4.0.1 on 2023-01-20 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bertConnector', '0007_uploaddocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploaddocument',
            name='documentId',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
