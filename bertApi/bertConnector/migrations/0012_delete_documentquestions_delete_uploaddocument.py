# Generated by Django 4.0.1 on 2023-01-24 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bertConnector', '0011_remove_uploaddocument_document_uploaddocument_note'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DocumentQuestions',
        ),
        migrations.DeleteModel(
            name='UploadDocument',
        ),
    ]
