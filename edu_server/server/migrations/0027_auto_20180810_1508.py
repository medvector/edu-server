# Generated by Django 2.0.7 on 2018-08-10 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0026_auto_20180807_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentstudyitem',
            name='relations_with_content_study_items',
            field=models.ManyToManyField(related_name='related_to', through='server.ContentStudyItem', to='server.ContentStudyItem'),
        ),
    ]
