# Generated by Django 2.0.7 on 2018-08-27 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0041_user_hub_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='scope',
        ),
    ]
