# Generated by Django 4.0.3 on 2022-04-27 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0034_remove_submit_contactor_submit_dealer'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatuslog',
            name='message',
            field=models.TextField(null=True),
        ),
    ]