from django.db import models
from django.contrib.postgres.fields import JSONField


class User(models.Model):
    login = models.CharField(max_length=128)
    hub_id = models.CharField(max_length=128, db_index=True, default=None)
    status = models.CharField(default='user', max_length=128)
    registration_date = models.DateTimeField(null=True, auto_now_add=True)

    access_token = models.CharField(null=True, default=None, max_length=256)
    access_token_updated_at = models.DateTimeField(auto_now=True)
    refresh_token = models.CharField(null=True, default=None, max_length=256)
    token_type = models.CharField(null=True, default=None, max_length=32)
    expires_in = models.PositiveIntegerField(null=True, default=3600)

    class Meta:
        db_table = "User"


class StudyItem(models.Model):
    visibility = models.CharField(default='public', max_length=32)
    updated_at = models.DateTimeField(auto_now=True)
    item_type = models.CharField(db_index=True, max_length=32)
    minimal_plugin_version = models.CharField(default='1.7-2018.1-119', max_length=256)

    class Meta:
        abstract = True


class InfoStudyItem(StudyItem):
    parent = models.ForeignKey('self', null=True, default=None, on_delete=models.CASCADE)

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
    relations_with_content_study_items = models.ManyToManyField('self', symmetrical=False,
                                                                through='ContentStudyItemsRelation')
    info_study_item = models.ForeignKey(InfoStudyItem, db_index=True, null=True, on_delete=models.CASCADE)

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
    child_position = models.PositiveIntegerField('order', default=0)
    is_new = models.BooleanField(default=True)

    class Meta:
        db_table = 'ContentStudyItemsRelation'
        ordering = ('child_position',)
