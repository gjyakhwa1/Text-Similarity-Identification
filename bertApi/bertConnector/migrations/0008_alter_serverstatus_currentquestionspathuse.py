# Generated by Django 4.0.1 on 2023-02-23 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bertConnector', '0007_auto_20230223_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverstatus',
            name='currentQuestionsPathUSE',
            field=models.CharField(default='./pickle_files/serializedIndex02', max_length=50, null=True),
        ),
    ]
