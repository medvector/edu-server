# Generated by Django 2.0.7 on 2018-08-14 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0029_auto_20180814_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(default='user', max_length=128),
        ),
    ]
