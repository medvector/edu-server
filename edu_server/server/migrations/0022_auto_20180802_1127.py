# Generated by Django 2.0.7 on 2018-08-02 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0021_auto_20180729_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiddenstudyitem',
            name='file',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='server.File'),
        ),
        migrations.AlterField(
            model_name='hiddenstudyitemsrelation',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='server.HiddenStudyItem'),
        ),
        migrations.AlterField(
            model_name='hiddenstudyitemsrelation',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='server.HiddenStudyItem'),
        ),
    ]
