# Generated by Django 2.0.7 on 2018-07-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_auto_20180724_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyitem',
            name='min_plugin_version',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
