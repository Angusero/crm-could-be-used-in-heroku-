# Generated by Django 3.0.5 on 2021-02-04 14:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_auto_20210204_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointshistory',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2, 2, 4, 23, 3, 32, 758425)),
        ),
    ]
