# Generated by Django 4.0.1 on 2022-02-06 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bertConnector', '0005_alter_question_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['id']},
        ),
    ]
