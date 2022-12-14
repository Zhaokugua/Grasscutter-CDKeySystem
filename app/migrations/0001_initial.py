# Generated by Django 3.2 on 2022-11-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CDKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=16)),
                ('cdk_value', models.TextField(null=True)),
                ('mail_template_id', models.IntegerField(default=0)),
                ('end_time', models.DateField(default='2022-10-1')),
                ('total_num', models.IntegerField(default=1)),
                ('used_num', models.IntegerField(default=0)),
                ('num_by_uid', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='CDkey_Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=16)),
                ('use_time', models.DateTimeField(auto_now=True)),
                ('user_uid', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Daily_Sign_Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_date', models.DateField(auto_now=True)),
                ('sign_uid', models.CharField(max_length=16)),
            ],
        ),
    ]
