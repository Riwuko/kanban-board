# Generated by Django 2.2.16 on 2020-09-24 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0002_auto_20200924_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
