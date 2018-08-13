import time

from debian.deb822 import OrderedSet
from django.db import models
from django.db.models import QuerySet

from .models import Description, File, InfoStudyItem, ContentStudyItem, ContentStudyItemsRelation
import json
from .Util import compare


class CourseManager:
    _meta_fields = {'version', 'format', 'language', 'programming_language'}
    _description_fields = {'title', 'description', 'description_format', 'summary', 'change_notes', 'type'}
    _stable_types = {'course', 'lesson', 'section'}
    _files_fields = {'course_files', 'test_files', 'task_files'}

    @staticmethod
    def _bytes_to_dict(data):
        course = json.loads(data.decode('utf-8'))
        if isinstance(course, str):
            course = json.loads(course)
        return course

    def _create_description(self, new_data, old_data=None):
        description = old_data if old_data is not None else dict()
        for key, value in new_data.items():
            if key in self._description_fields:
                description[key] = value
        return description

    """
        Temporary help function
    """

    @staticmethod
    def _clean_database():
        ContentStudyItemsRelation.objects.all().delete()
        ContentStudyItem.objects.all().delete()
        Description.objects.all().delete()
        File.objects.all().delete()
        InfoStudyItem.objects.all().delete()
        return True


class CourseWriter(CourseManager):
    def _create_item_file(self, item_info, meta_info, old_file=None, update_old=False):
        if item_info['type'] in {'section', 'lesson'}:
            return None

        file = dict() if old_file is None else old_file.data
        updated_any_field = False

        for field in item_info:
            if field in self._files_fields:
                updated_any_field = True
                file[field] = item_info[field]

        if not updated_any_field:
            return old_file

        if update_old:
            old_file.data = file
            old_file.save()
            return old_file

        file = File.objects.create(programming_language=meta_info['programming_language'], data=file)

        return file

    def _create_item(self, item_info, meta_info, info_parent=None, content_parent=None, position=0):
        version = meta_info['format']

        item_type = item_info['type'] if item_info['type'] in self._stable_types else 'task'
        info_item = InfoStudyItem.objects.create(item_type=item_type, minimal_plugin_version=version,
                                                 parent=info_parent)

        description = Description.objects.create(data=self._create_description(item_info),
                                                 human_language=meta_info['language'])

        file = self._create_item_file(item_info, meta_info)

        content_item = ContentStudyItem.objects.create(info_study_item=info_item, item_type=item_type, file=file,
                                                       description=description, minimal_plugin_version=version)

        if content_parent is not None:
            ContentStudyItemsRelation.objects.create(parent=content_parent, child=content_item, child_position=position)

        response = {'id': info_item.id, 'type': item_info['type']}
        if 'items' in item_info:
            response['items'] = list()
            for position, item in enumerate(item_info['items']):
                response['items'].append(self._create_item(item_info=item, meta_info=meta_info, info_parent=info_item,
                                                           content_parent=content_item, position=position))

        return response

    def create_course(self, data):
        course_data = self._bytes_to_dict(data=data)
        meta_info = {key: value for key, value in course_data.items() if key in self._meta_fields}
        course = self._create_item(item_info=course_data, meta_info=meta_info)
        return course

    def _update_content_item(self, item_info, meta_info, info_item, content_parent, content_child, position):
        if 'type' in item_info and item_info['type'] == 'course':
            content_child.description.data = self._create_description(new_data=item_info,
                                                                      old_data=content_child.description.data)
            content_child.description.save()

            content_child.file = self._create_item_file(item_info=item_info, meta_info=meta_info,
                                                        old_file=content_child.file, update_old=True)
            content_child.save()
            return content_child

        relation = ContentStudyItemsRelation.objects.get(parent_id=content_parent.id, child_id=content_child.id)

        if relation.is_new and relation.child.item_type != 'task':
            relation.child_position = position
            relation.save()

            content_child.description.data = self._create_description(new_data=item_info,
                                                                      old_data=content_child.description.data)
            content_child.description.save()

            return content_child
        else:
            relation.delete()
            return self._create_content_item(item_info=item_info, meta_info=meta_info, info_item=info_item,
                                             content_parent=content_parent, content_child=content_child,
                                             position=position)

    def _create_content_item(self, item_info, meta_info, info_item, content_child, content_parent=None, position=0):
        if len(item_info) == 1:
            ContentStudyItemsRelation.objects.create(parent=content_parent, child=content_child,
                                                     child_position=position, is_new=False)
            return content_child
        else:
            version = meta_info['format']
            description = self._create_description(new_data=item_info, old_data=content_child.description.data)
            description = Description.objects.create(data=description, human_language=meta_info['language'])

            item_type = item_info['type'] if 'type' in item_info else content_child.item_type
            if item_type not in self._stable_types:
                item_type = 'task'

            item_info['type'] = item_type
            old_file = None if content_child.file is None else content_child.file
            new_file = self._create_item_file(item_info=item_info, meta_info=meta_info, old_file=old_file)

            new_content_item = ContentStudyItem.objects.create(info_study_item=info_item, item_type=item_type,
                                                               description=description, minimal_plugin_version=version,
                                                               file=new_file)

            if content_parent is not None:
                ContentStudyItemsRelation.objects.create(parent=content_parent, child=new_content_item,
                                                         child_position=position)
            return new_content_item

    def _update_item(self, item_info, meta_info, info_parent, content_parent=None, position=0, create_new=False):
        if 'id' in item_info:
            info_item = InfoStudyItem.objects.get(id=item_info['id'])
            current_content_item = info_item.contentstudyitem_set.order_by('-updated_at').first()

            response = {'id': info_item.id}

            if create_new:
                new_content_item = self._create_content_item(item_info=item_info, meta_info=meta_info,
                                                             info_item=info_item, content_parent=content_parent,
                                                             content_child=current_content_item, position=position)
            else:
                new_content_item = self._update_content_item(item_info=item_info, meta_info=meta_info,
                                                             info_item=info_item, content_parent=content_parent,
                                                             content_child=current_content_item, position=position)

            if 'items' in item_info:
                response['items'] = list()
                for position, subitem in enumerate(item_info['items']):
                    response['items'].append(self._update_item(item_info=subitem, meta_info=meta_info,
                                                               position=position, info_parent=info_item,
                                                               content_parent=new_content_item, create_new=create_new))

            return response
        else:
            return self._create_item(item_info=item_info, meta_info=meta_info, position=position,
                                     info_parent=info_parent, content_parent=content_parent)

    def update_course(self, data, course_id):
        course_data = self._bytes_to_dict(data=data)
        course_data['id'] = course_id

        meta_info = {key: value for key, value in course_data.items() if key in self._meta_fields}

        course = InfoStudyItem.objects.get(id=course_data['id'])
        content_course = course.contentstudyitem_set.all().order_by('-updated_at').first()

        if compare(course_data['format'], content_course.minimal_plugin_version) < 0:
            create_new = True
        else:
            create_new = False

        if create_new:
            content_course = None

        return self._update_item(item_info=course_data, meta_info=meta_info, info_parent=course,
                                 content_parent=content_course, create_new=create_new)


class CourseGetter(CourseManager):
    @staticmethod
    def get_item_version(queryset, suitable_version=None):
        if suitable_version is None:
            return queryset.order_by('-updated_at').first()

        current_version = None

        for item in queryset:
            if compare(item.minimal_plugin_version, suitable_version) <= 0:
                if current_version is None:
                    current_version = item
                elif compare(current_version.minimal_plugin_version, item.minimal_plugin_version) < 0:
                    current_version = item

        return current_version

    def get_all_courses_info(self, suitable_version=None):
        response = {'courses': list()}
        courses = InfoStudyItem.objects.filter(item_type='course')

        for course in courses:
            if suitable_version is not None and compare(course.minimal_plugin_version, suitable_version) > 0:
                continue

            course_version = self.get_item_version(course.contentstudyitem_set.all(), suitable_version)

            course_info = self._get_content_item(course_version, add_files=False, add_subitems=False)

            response['courses'].append(course_info)
        return response

    @staticmethod
    def _get_subitems(item, response, get_function):
        if item.item_type == 'task':
            return response

        subitems = item.relations_with_content_study_items.order_by('child')

        response['items'] = list()
        for subitem in subitems:
            response['items'].append(get_function(subitem))

        return response

    @staticmethod
    def _get_standard_fields(content_item):
        response = {'id': content_item.info_study_item.id,
                    'last_modified': str(content_item.updated_at),
                    'format': content_item.minimal_plugin_version}

        if content_item.item_type != 'task':
            response['type'] = content_item.item_type
        else:
            response['version_id'] = content_item.id
            response['type'] = content_item.description.data['type']

        return response

    def _get_content_item(self, content_item, add_files=True, add_subitems=True):
        response = self._get_standard_fields(content_item)

        response.update(content_item.description.data)

        if add_files and content_item.item_type not in {'section', 'lesson'}:
            response.update(content_item.file.data)

        if content_item.item_type == 'course':
            response['programming_language'] = content_item.file.programming_language
            response['language'] = content_item.description.human_language

        if add_subitems:
            response = self._get_subitems(item=content_item, response=response, get_function=self._get_content_item)
        return response

    def get_content_item_delta(self, content_item):
        response = self._get_standard_fields(content_item)
        response = self._get_subitems(item=content_item, response=response, get_function=self.get_content_item_delta)
        return response

    def check_item(self, info_item_id, info_item_type, version=None):
        """
        :param info_item_id: id from httprequest
        :param info_item_type: type from httprequest
        :param version: suitable plugin version
        :return: (result, http_code)
        result can be None or ContentStudyItem
        current http-codes:
        200 - there is such item in database,
        404 - there is no item with such id in database,
        409 - item type with such id is not the same as type in http-request
        """

        try:
            info_item = InfoStudyItem.objects.get(id=info_item_id)
        except models.ObjectDoesNotExist:
            return None, 404

        if info_item.item_type != info_item_type:
            return None, 409

        content_item = self.get_item_version(info_item.contentstudyitem_set.all(), version)
        return content_item, 200

    def check_several_items(self, item_id_list, items_type):
        field = items_type + 's'
        response = {field: list()}
        for item_id in item_id_list:
            current_item, code = self.check_item(item_id, items_type)
            if code == 200:
                response[field].append(self._get_content_item(current_item))
            else:
                return current_item, code
        return response, 200
