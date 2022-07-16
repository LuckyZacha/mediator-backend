# Generated by Django 4.0.4 on 2022-07-21 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0030_alter_post_author'),
        ('Paper', '0046_alter_status_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_type', to='Account.businesstype'),
        ),
    ]
