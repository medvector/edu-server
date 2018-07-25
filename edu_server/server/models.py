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
    @staticmethod
    def _bytes_to_dict(data):
        course = json.loads(data.decode('utf-8'))
        if type(course) is str:
            course = json.loads(course)
        return course

    @staticmethod
    def version_to_number(version):
        version = version.split('-')
        f, s, t = [version[i].split('.') for i in range(len(version))]
        # yes, i know
        number = ''.join([''.join(f), s[0], '0' * (2 - len(s[1])), s[1], '0' * (3 - len(t[0])), t[0]])
        return number

    def create_item(self, item, item_type, visibility=True, min_plugin_version=None, *args, **kwargs):
        # to do: change into relation between item and description
        item_data = {key: value for key, value in item.items() if key != 'items'}
        study_item = self.model(min_plugin_version=min_plugin_version, item_type=item_type,
                                data=item_data, visibility=visibility)
        study_item.save()
        return study_item

    def create_task(self, task_data, parent, task_position):
        task = self.create_item(item=task_data, item_type='task')
        task_version = self.create_item(item=task_data, item_type='task_version')
        parent.create_relation(child=task, position=task_position)
        task.create_relation(child=task_version, position=0)
        return {'id': task.id}

    def create_lesson(self, lesson_data, parent, lesson_position):
        lesson = self.create_item(item=lesson_data, item_type='lesson')
        parent.create_relation(child=lesson, position=lesson_position)
        response = {'id': lesson.id, 'items': []}
        for position, item in enumerate(lesson_data['items']):
            response['items'].append(self.create_task(item, lesson, position))
        return response

    def create_section(self, section_data, parent, section_position):
        section = self.create_item(item=section_data, item_type='section')
        parent.create_relation(child=section, position=section_position)
        response = {'id': section.id, 'items': []}
        for position, item in enumerate(section_data['items']):
            response['items'].append(self.create_lesson(item, section, position))
        return response

    def create_course(self, course_data):
        course_info = self._bytes_to_dict(course_data)
        course = self.create_item(item=course_info, item_type='course')
        print(self.version_to_number(course_info['version']))
        course_version = self.create_item(item=course_info, min_plugin_version=course_info['version'],
                                          item_type='course_version', visibility=False)
        course.create_relation(course_version, 0)
        response = {'id': course.id, 'items': []}
        for position, item in enumerate(course_info['items']):
            if item['type'] == 'section':
                response['items'].append(self.create_section(item, course_version, position))
            else:
                response['items'].append(self.create_lesson(item, course_version, position))
        return response

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

    def get_course(self, course_id):
        course = self.filter(id=course_id)
        if len(course) == 0:
            return 404
        elif course[0].item_type != 'course':
            return 409

        course_version = course[0].relations_in_graph.all().order_by('-updated_at')[0]

        response = course_version.data
        response['id'] = course_id
        response['items'] = list()
        for course_item in course_version.relations_in_graph.all():
            if course_item.item_type == 'section':
                response['items'].append(self.get_section(course_item.id))
            elif course_item.item_type == 'lesson':
                response['items'].append(self.get_lesson(course_item.id))

        return response

    def get_section(self, section_id):
        section = self.filter(id=section_id)
        if len(section) == 0:
            return 404
        elif section[0].item_type != 'section':
            return 409

        section = section[0]
        response = section.data
        response['id'] = section.id
        response['items'] = list()

        for lesson in section.relations_in_graph.all():
            response['items'].append(self.get_lesson(lesson.id))

        return response

    def get_lesson(self, lesson_id):
        lesson = self.filter(id=lesson_id)
        if len(lesson) == 0:
            return 404
        elif lesson[0].item_type != 'lesson':
            return 409

        lesson = lesson[0]
        response = lesson.data
        response['id'] = lesson.id
        response['items'] = list()

        for task in lesson.relations_in_graph.all():
            response['items'].append(self.get_task(task.id))

        return response

    def get_task(self, task_id):
        task = self.filter(id=task_id)
        if len(task) == 0:
            return 404
        elif task[0].item_type != 'task':
            return 409

        task = task[0]
        task_version = task.relations_in_graph.all().order_by('-updated_at')[0]
        return task_version.data


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
