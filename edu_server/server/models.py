from django.db import models
from django.contrib.postgres.fields import JSONField


class StudyItem(models.Model):
    visibility = models.CharField(default='public', max_length=32)
    updated_at = models.DateTimeField(auto_now=True)
    item_type = models.CharField(max_length=32)
    minimal_plugin_version = models.CharField(default='1.7-2018.1-119', max_length=256)

    class Meta:
        abstract = True


class InfoStudyItem(StudyItem):
    parent = models.ForeignKey('self', null=True, default=None, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'InfoStudyItem'


class Description(models.Model):
    human_language = models.CharField(default='en', max_length=32)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField()

    class Meta:
        db_table = 'Description'


class File(models.Model):
    programming_language = models.CharField(max_length=32)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField()

    class Meta:
        db_table = 'File'


class ContentStudyItem(StudyItem):
    relations_with_content_study_items = models.ManyToManyField('self', through='ContentStudyItem',
                                                                symmetrical=False)
    info_study_item = models.ForeignKey(InfoStudyItem, null=True, on_delete=models.DO_NOTHING)

    """
        When additional human and programming languages are added these fields
        may change to many-to-many
    """
    description = models.ForeignKey(Description, on_delete=models.DO_NOTHING)
    file = models.ForeignKey(File, null=True, default=None, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ContentStudyItem'


class ContentStudyItemsRelation(models.Model):
    parent = models.ForeignKey(ContentStudyItem, related_name='parent', on_delete=models.CASCADE)
    child = models.ForeignKey(ContentStudyItem, related_name='child', on_delete=models.CASCADE)
    child_position = models.IntegerField(default=0)
    is_new = models.BooleanField(default=True)

    class Meta:
        db_table = 'ContentStudyItemsRelation'
