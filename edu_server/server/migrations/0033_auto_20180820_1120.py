# Generated by Django 2.0.7 on 2018-08-20 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0032_auto_20180820_1104'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='contentstudyitemsrelation',
            index_together={('parent', 'child_position')},
        ),
    ]
