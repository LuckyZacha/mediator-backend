# Generated by Django 4.0.4 on 2022-08-04 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0052_journal_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequency',
            name='name',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
