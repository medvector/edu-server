from django.db import models
from django.contrib.postgres.fields import JSONField
from django.http import HttpRequest, HttpResponse
import json


# Create your models here.


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=128)
    tag_type = models.CharField(max_length=128)

    class Meta:
        db_table = 'Tags'

    def __str__(self):
        return 'tag: {}, type: {}'.format(self.title, self.tag_type)


class StudyItemManager(models.Manager):
    @staticmethod
    def _bytes_to_dict(data):
        course = dict()
        course = json.loads(data.decode('utf-8'))
        if type(course) is str:
            course = json.loads(course)
        return course

    def create_item(self, minimal_plugin_version, item_type,
                    item_data, visibility, *args, **kwargs):
        study_item = self.model(minimal_plugin_version=minimal_plugin_version,
                                study_item_type=item_type, data=item_data,
                                visibility=visibility)
        study_item.save()
        return study_item

    def look_through_items(self, items, minimal_plugin_version, visibility):
        created_items = []
        for item in items:
            item_info = {'title': item['title'],
                         'description': item['description'],
                         'description_format': item['description_format']}
            created_item = self.create_item(minimal_plugin_version=minimal_plugin_version,
                                            item_type=item['type'], item_data=item_info,
                                            visibility=visibility)
            created_items.append(created_item)
            if 'items' in item:
                children = self.look_through_items(item['items'], minimal_plugin_version, visibility)
                created_item.create_relations(children)
        return created_items

    def save_new_course(self, data):
        course_structure = StudyItemManager._bytes_to_dict(data=data)
        course_info = {'title': course_structure['title'],
                       'summary': course_structure['summary'],
                       'language': course_structure['language'],
                       'change_notes': course_structure['change_notes'],
                       'course_files': course_structure['course_files'],
                       'programming_language': course_structure['programming_language']}
        course = self.create_item(minimal_plugin_version=course_structure['version'],
                                  item_type='course', item_data=course_info, visibility='public')
        children = self.look_through_items(course_structure['items'], course_structure['version'], 'public')
        course.create_relations(children)
        return True


class StudyItem(models.Model):
    minimal_plugin_version = models.CharField(max_length=128)
    study_item_type = models.CharField(max_length=128)
    data = JSONField(null=True)
    creation_date = models.DateTimeField(auto_created=True)
    edition_date = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=128)
    objects = StudyItemManager()

    # tags = models.ManyToManyField(Tag)
    relations_in_graph = models.ManyToManyField('self', through='StudyItemsRelation', related_name='related_to',
                                                symmetrical=False)

    class Meta:
        db_table = 'StudyItems'

    def __str__(self):
        return self.study_item_type

    def create_relations(self, children):
        for position, child in enumerate(children):
            StudyItemsRelation.objects.create(parent=self, child_id=child, child_position=position)
        return True


class StudyItemsRelation(models.Model):
    parent = models.ForeignKey(StudyItem, related_name='parent', on_delete=models.DO_NOTHING)
    child = models.ForeignKey(StudyItem, related_name='child', on_delete=models.DO_NOTHING)
    child_position = models.IntegerField()

    class Meta:
        db_table = 'StudyItemsRelations'
