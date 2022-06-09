# Generated by Django 4.0.4 on 2022-06-10 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0019_unitbusiness'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='businesses',
            field=models.ManyToManyField(blank=True, through='Account.UnitBusiness', to='Account.businesstype'),
        ),
        migrations.AddField(
            model_name='unit',
            name='phone_number',
            field=models.CharField(max_length=255, null=True),
        ),
    ]