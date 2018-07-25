from django.db import models
from django.db.models import Max
from django.contrib.postgres.fields import JSONField
from django.http import HttpRequest, HttpResponse
import json


# Create your models here.


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=128)
    tag_type = models.CharField(max_length=128)

    class Meta:
        db_table = 'Tags'

    def __unicode__(self):
        return 'tag: {}, type: {}'.format(self.title, self.tag_type)


standard_types = {'course', 'section', 'lesson'}


class StudyItemManager(models.Manager):
    _types_with_fake_children = {'course', 'task'}
    _stable_types = {'course', 'section', 'lesson'}
    _meta_fields = {'version', 'language', 'programming_language'}
    _description_fields = {'description', 'description_format', 'summary',
                           'change_notes', 'title', 'course_files', 'format'}

    @staticmethod
    def _bytes_to_dict(data):
        course = json.loads(data.decode('utf-8'))
        if type(course) is str:
            course = json.loads(course)
        return course

    @staticmethod
    def _version_to_number(version):
        version = version.split('-')
        f, s, t = [version[i].split('.') for i in range(len(version))]
        # yes, i know
        number = ''.join([''.join(f), s[0], '0' * (2 - len(s[1])), s[1], '0' * (3 - len(t[0])), t[0]])
        return number

    def _create_item(self, item_info, meta_info, position=0, parent=None):
        item_type = item_info['type'] if item_info['type'] in self._stable_types else 'task'
        item_data = {key: value for key, value in item_info.items() if key in self._description_fields}

        item = self.model(min_plugin_version=meta_info['version'], item_type=item_type,
                          data=item_data, visibility=True)
        item.save()
        item_id = item.id

        if item_type in self._types_with_fake_children:
            fake = self.model(min_plugin_version=meta_info['version'], item_type=item_type,
                                data=None, visibility=True)
            fake.save()
            item.item_type = item_type + '_version'
            item.save()
            fake.create_relation(child=item, position=position)
            item_id = fake.id
            if parent:
                parent.create_relation(child=fake, position=position)
        else:
            parent.create_relation(child=item, position=position)

        response = {'id': item_id}
        if 'items' in item_info:
            response['items'] = list()
            for position, subitem in enumerate(item_info['items']):
                response['items'].append(self._create_item(item_info=subitem, meta_info=meta_info,
                                                            position=position, parent=item))

        return response

    def create_course(self, data):
        course_data = self._bytes_to_dict(data)
        meta_info = {key: value for key, value in course_data.items() if key in self._meta_fields}
        course = self._create_item(course_data, meta_info)
        return course

    def get_all_courses_info(self):
        response = {'courses': []}
        for course in self.filter(item_type='course_version'):
            # it looks so horrible now, need look for change
            parent = StudyItemsRelation.objects.filter(child_id=course.id)[0].parent.id
            current_course_info = {'id': parent, 'version': course.min_plugin_version}
            for key, value in course.data.items():
                if key != 'course_files':
                    current_course_info[key] = value
            response['courses'].append(current_course_info)
        return response

    def _get_item(self, item_id, item_type):
        item = self.filter(id=item_id)
        if len(item) == 0:
            return 404
        elif item[0].item_type != item_type:
            return 409

        if item_type in self._types_with_fake_children:
            item = item[0].relations_in_graph.all().order_by('-updated_at')[0]
        else:
            item = item[0]

        response = item.data
        response['id'] = item_id
        response['type'] = item.item_type

        subitems = item.relations_in_graph.all()
        if len(subitems) > 0:
            response['items'] = list()
            for subitem in subitems:
                response['items'].append(self.get_item(subitem.id, subitem.item_type))
        return response

    def get_course(self, course_id):
        return self._get_item(item_id=course_id, item_type='course')

    def get_section(self, section_id):
        return self._get_item(item_id=section_id, item_type='section')

    def get_lesson(self, lesson_id):
        return self._get_item(item_id=lesson_id, item_type='lesson')

    def get_task(self, task_id):
        return self._get_item(item_id=task_id, item_type='task')


class StudyItem(models.Model):
    min_plugin_version = models.CharField(max_length=128, null=True)
    item_type = models.CharField(max_length=128)
    data = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.BooleanField(default=True)
    objects = StudyItemManager()

    # tags = models.ManyToManyField(Tag)
    relations_in_graph = models.ManyToManyField('self', through='StudyItemsRelation',
                                                related_name='related_to', symmetrical=False)

    class Meta:
        db_table = 'StudyItems'
        # ordering = ['-creation_date']

    def __unicode__(self):
        return self.item_type

    def create_relation(self, child, position):
        StudyItemsRelation.objects.create(parent=self, child=child, child_position=position)


class Description(models.Model):
    human_language = models.CharField(max_length=128)
    edit_date = models.DateTimeField(auto_now_add=True)
    data = JSONField(null=False)
    study_item = models.ForeignKey(StudyItem, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Description'


class StudyItemsRelation(models.Model):
    parent = models.ForeignKey(StudyItem, related_name='parent', on_delete=models.DO_NOTHING)
    child = models.ForeignKey(StudyItem, related_name='child', on_delete=models.DO_NOTHING)
    child_position = models.IntegerField()

    class Meta:
        db_table = 'StudyItemsRelations'
