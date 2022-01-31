# Generated by Django 3.2.5 on 2022-01-26 15:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0013_alter_shopuser_activation_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 28, 15, 11, 10, 152919, tzinfo=utc), null=True),
        ),
    ]
