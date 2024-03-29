# Generated by Django 3.0.5 on 2021-02-04 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_auto_20210204_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointshistory',
            name='expiration_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 5, 0, 2, 56, 319165)),
        ),
        migrations.AlterField(
            model_name='pointshistory',
            name='point_add',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='pointshistory',
            name='point_use',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='pointshistory',
            name='points_after',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
