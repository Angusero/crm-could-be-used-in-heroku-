# Generated by Django 3.0.5 on 2021-03-02 01:29

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_auto_20210228_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointshistory',
            name='expiration_date',
            field=models.DateTimeField(default=accounts.models.inTwoYears),
        ),
    ]
