# Generated by Django 3.0.5 on 2021-02-04 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20210204_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointshistory',
            name='points_before',
        ),
    ]