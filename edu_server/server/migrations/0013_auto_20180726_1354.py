# Generated by Django 2.0.7 on 2018-07-26 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_studyitem_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyitem',
            name='version',
            field=models.BigIntegerField(default=17201801119),
        ),
    ]
