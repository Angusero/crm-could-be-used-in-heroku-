# Generated by Django 3.0.5 on 2020-10-12 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200926_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
