# Generated by Django 3.0.4 on 2020-05-06 11:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200505_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 5, 6, 11, 43, 9, 451856, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contribution',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contribution',
            name='registration_period',
            field=models.CharField(choices=[('n', 'Normal'), ('l', 'Late')], default='n', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contribution',
            name='user',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]