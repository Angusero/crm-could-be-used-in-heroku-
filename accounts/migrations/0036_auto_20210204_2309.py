# Generated by Django 3.0.5 on 2021-02-04 14:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_pointshistory_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointshistory',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 4, 23, 9, 17, 680835)),
        ),
    ]
