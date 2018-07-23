# Generated by Django 2.0.7 on 2018-07-22 15:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_created=True)),
                ('minimal_plugin_version', models.CharField(max_length=128)),
                ('study_item_type', models.CharField(max_length=128)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('edition_date', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.CharField(max_length=128)),
                ('relation_in_graph', models.ManyToManyField(related_name='_studyitem_relation_in_graph_+', to='server.StudyItem')),
            ],
            options={
                'db_table': 'StudyItems',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('tag_type', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='studyitem',
            name='tags',
            field=models.ManyToManyField(to='server.Tag'),
        ),
    ]
