# Generated by Django 4.0.1 on 2023-01-24 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_approved',
            field=models.BooleanField(),
        ),
    ]
