# Generated by Django 3.1.3 on 2020-12-13 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_auto_20201213_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='utc_time',
            field=models.IntegerField(default=0),
        ),
    ]
