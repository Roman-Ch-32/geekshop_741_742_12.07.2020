# Generated by Django 3.2.5 on 2022-02-10 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210811_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='href',
        ),
    ]
