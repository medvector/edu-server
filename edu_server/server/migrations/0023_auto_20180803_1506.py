# Generated by Django 2.0.7 on 2018-08-03 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0022_auto_20180802_1127'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RealStudyItem',
            new_name='InfoStudyItem',
        ),
        migrations.RenameField(
            model_name='hiddenstudyitem',
            old_name='real_study_item',
            new_name='info_study_item',
        ),
        migrations.AlterModelTable(
            name='infostudyitem',
            table='InfoStudyItem',
        ),
    ]
