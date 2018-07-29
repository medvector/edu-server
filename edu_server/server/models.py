from django.db import models
from django.db.models import Max
from django.contrib.postgres.fields import JSONField
from django.http import HttpRequest, HttpResponse
import json


class StudyItem(models.Model):
    visibility = models.CharField(default='public', max_length=32)
    updated_at = models.DateTimeField(auto_now=True)
    item_type = models.CharField(max_length=32)
    minimal_plugin_version = models.BigIntegerField(null=True)

    class Meta:
        abstract = True


class RealStudyItem(StudyItem):
    parent = models.ForeignKey('self', null=True, default=None, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'RealStudyItem'


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


class HiddenStudyItem(StudyItem):
    relations_with_hidden_study_items = models.ManyToManyField('self', symmetrical=False,
                                                               through='HiddenStudyItemsRelation')
    real_study_item = models.ForeignKey(RealStudyItem, null=True, on_delete=models.DO_NOTHING)

    """
        When additional human and programming languages are added these fields
        need change to Many-to-Many(not exactly)
    """
    description = models.ForeignKey(Description, on_delete=models.DO_NOTHING)
    file = models.ForeignKey(File, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'HiddenStudyItem'


class HiddenStudyItemsRelation(models.Model):
    parent = models.ForeignKey(HiddenStudyItem, related_name='parent', on_delete=models.DO_NOTHING)
    child = models.ForeignKey(HiddenStudyItem, related_name='child', on_delete=models.DO_NOTHING)
    child_position = models.IntegerField(default=0)
    is_new = models.BooleanField(default=True)

    class Meta:
        db_table = 'HiddenStudyItemsRelation'


class CourseManager:
    _meta_fields = {'version', 'language', 'programming_language'}

    @staticmethod
    def _bytes_to_dict(data):
        course = json.loads(data.decode('utf-8'))
        if isinstance(course, str):
            course = json.loads(course)
        return course

    """
        Following two functions will be deleted in several days.
        Now it's simple way to compare different plugin versions.
    """

    @staticmethod
    def _version_to_number(version):
        version = version.split('-')
        f, s, t = [version[i].split('.') for i in range(len(version))]
        number = ''.join([''.join(f), s[0], '0' * (2 - len(s[1])), s[1], '0' * (3 - len(t[0])), t[0]])
        return int(number)

    @staticmethod
    def _number_to_version(number):
        version = str(number)[::-1]
        f = (version[0:3])[::-1].strip('0')
        s = (version[3:5])[::-1].strip('0')
        year = (version[5:9])[::-1]
        t = (version[9:])[::-1]
        version = ''.join([t[0], '.', t[1:], '-', year, '.', s, '-', f])
        return version

    def _create_item(self, item_info, meta_info, real_parent=None, hidden_parent=None, position=0):
        version = self._version_to_number(meta_info['version'])
        real_item = RealStudyItem.objects.create(item_type=item_info['type'], minimal_plugin_version=version,
                                                 parent=real_parent)

        description = Description.objects.create(data=item_info['description'], human_language=meta_info['language'])

        if 'course_files' in item_info:
            file = File.objects.create(programming_language=meta_info['programming_language'],
                                       data=item_info['course_files'])
        else:
            file = None

        hidden_item = HiddenStudyItem.objects.create(real_study_item=real_item, item_type=item_info['type'], file=file,
                                                     description=description, minimal_plugin_version=version)

        if hidden_parent is not None:
            HiddenStudyItemsRelation.objects.create(parent=hidden_parent, child=hidden_item, child_position=position)

        response = {'id': real_item.id}
        if 'items' in item_info:
            response['items'] = list()
            for position, item in enumerate(item_info['items']):
                response['items'].append(self._create_item(item_info=item, meta_info=meta_info, real_parent=real_item,
                                                           hidden_parent=hidden_item, position=position))

        return response

    def create_course(self, data):
        course_data = self._bytes_to_dict(data=data)
        meta_info = {key: value for key, value in course_data.items() if key in self._meta_fields}
        course = self._create_item(item_info=course_data, meta_info=meta_info)
        return course

    def _update_existing_item(self, item_info, meta_info, position=0, real_parent=None, hidden_parent=None):
        if 'id' in item_info:
            real_item = RealStudyItem.objects.get(id=item_info['id'])
            hidden_item = real_item.hiddenstudyitem_set.order_by('-updated_at')[0]

            if hidden_parent is not None:
                relation = HiddenStudyItemsRelation.objects.filter(parent_id=hidden_parent.id, child_id=hidden_item.id)[
                    0]
                relation.child_position = position
                relation.save()

            response = {'id': real_item.id}

            if len(item_info) > 1:
                if 'description' in item_info:
                    hidden_item.description.data = item_info['description']
                    hidden_item.description.save()

                if 'course_files' in item_info:
                    hidden_item.file.data = item_info['course_files']
                    hidden_item.file.save()

                if 'items' in item_info:
                    response['items'] = list()
                    for position, subitem in enumerate(item_info['items']):
                        response['items'].append(self._update_existing_item(item_info=subitem, meta_info=meta_info,
                                                                            position=position, real_parent=real_item,
                                                                            hidden_parent=hidden_item))

            return response
        else:
            return self._create_item(item_info=item_info, meta_info=meta_info, position=position,
                                     real_parent=real_parent, hidden_parent=hidden_parent)

    def _create_new_hidden_item(self, item_info, meta_info, position=0, real_parent=None, hidden_parent=None):
        if 'id' in item_info:
            real_item = RealStudyItem.objects.get(id=item_info['id'])
            hidden_item = real_item.hiddenstudyitem_set.order_by('-updated_at')[0]

            if len(item_info) == 1:
                HiddenStudyItemsRelation.objects.create(parent=hidden_parent, child=hidden_item,
                                                        child_position=position)
                return {'id': real_item.id}
            else:
                version = self._version_to_number(meta_info['version'])
                if 'description' in item_info:
                    description = Description.objects.create(data=item_info['description'],
                                                             human_language=meta_info['language'])
                else:
                    description = hidden_item.description

                if 'course_files' in item_info:
                    file = File.objects.create(programming_language=meta_info['programming_language'],
                                               data=item_info['course_files'])
                else:
                    file = hidden_item.file

                item_type = item_info['type'] if 'type' in item_info else hidden_item.item_type
                new_hidden_item = HiddenStudyItem.objects.create(real_study_item=real_item, item_type=item_type,
                                                                 file=file, description=description,
                                                                 minimal_plugin_version=version)

                if hidden_parent is not None:
                    HiddenStudyItemsRelation.objects.create(parent=hidden_parent, child=new_hidden_item,
                                                            child_position=position)

                response = {'id': real_item.id}
                if 'items' in item_info:
                    response['items'] = list()
                    for position, item in enumerate(item_info['items']):
                        response['items'].append(
                            self._create_new_hidden_item(item_info=item, meta_info=meta_info, real_parent=real_item,
                                                         hidden_parent=new_hidden_item, position=position))

                return response
        else:
            return (self._create_item(item_info=item_info, meta_info=meta_info, position=position,
                                      real_parent=real_parent, hidden_parent=hidden_parent))

    def update_course(self, data):
        course_data = self._bytes_to_dict(data=data)
        meta_info = {key: value for key, value in course_data.items() if key in self._meta_fields}
        course = RealStudyItem.objects.get(id=course_data['id'])
        hidden_course = course.hiddenstudyitem_set.all().order_by('-updated_at')[0]
        create = self._version_to_number(course_data['version']) > hidden_course.minimal_plugin_version
        if not create:
            return self._update_existing_item(item_info=course_data, meta_info=meta_info)
        else:
            return self._create_new_hidden_item(item_info=course_data, meta_info=meta_info)

    def get_all_courses_info(self, version=None):
        response = {'courses': list()}
        courses = RealStudyItem.objects.filter(item_type='course')

        if version is not None:
            version = self._version_to_number(version=version)
            courses = courses.filter(minimal_plugin_version__lte=version)

        for course in courses:
            course_version = course.hiddenstudyitem_set.order_by('-updated_at')
            if version is not None:
                course_version = course.hiddenstudyitem_set.filter(minimal_plugin_version__lte=version)
                course_version = course_version.order_by('-minimal_plugin_version')
            course_version = course_version[0]
            version = self._number_to_version(course.minimal_plugin_version)
            course_info = {'id': course_version.id, 'version': version,
                           'description': course_version.description.data}
            response['courses'].append(course_info)
        return response

    def _get_hidden_item(self, item):
        response = {'id': item.id, 'type': item.item_type, 'description': item.description.data}
        subitems = item.relations_with_hidden_study_items.all()
        if len(subitems):
            response['items'] = list()
            for subitem in subitems:
                response['items'].append(self._get_hidden_item(subitem))
        return response

    def _check_hidden_item(self, item_id, item_type):
        item = HiddenStudyItem.objects.filter(id=item_id)
        if len(item) == 0:
            return 404
        elif item[0].item_type != item_type:
            return 409
        return self._get_hidden_item(item[0])

    def _check_several_hidden_items(self, item_id_list, items_type):
        field = items_type + 's'
        response = {field: list()}
        for item_id in item_id_list:
            current = self._check_hidden_item(item_id, items_type)
            if isinstance(current, dict):
                response[field].append(current)
            else:
                return current
        return response
