# Generated by Django 4.0.1 on 2023-01-20 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bertConnector', '0009_alter_uploaddocument_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('documentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bertConnector.uploaddocument', to_field='documentId')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]