# Generated by Django 3.2 on 2022-11-15 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_cdkey_record_use_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdkey',
            name='num_by_uid',
            field=models.IntegerField(default=1),
        ),
    ]
