# Generated by Django 3.0.4 on 2020-05-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_contribution_registration_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]