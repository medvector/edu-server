# Generated by Django 2.0.7 on 2018-07-23 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_remove_studyitem_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studyitem',
            name='relations_in_graph',
        ),
    ]
