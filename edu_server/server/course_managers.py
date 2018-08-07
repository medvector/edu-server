from django.db import models
from django.db.models import QuerySet

from server.models import Description, File, InfoStudyItem, ContentStudyItem, ContentStudyItemsRelation
import json
from server.Util import compare

class CourseManager:
    _meta_fields = {'version', 'format', 'language', 'programming_language'}
    _description_fields = {'title', 'description', 'description_format', 'summary', 'format', 'change_notes', 'type'}
    _stable_types = {'course', 'lesson', 'section'}

    @staticmethod
    def _bytes_to_dict(data):
        course = json.loads(data.decode('utf-8'))
        if isinstance(course, str):
            course = json.loads(course)
        return course

    def _get_description(self, new_data, old_data=None):
        description = old_data if old_data is not None else dict()
        for key, value in new_data.items():
            if key in self._description_fields:
                description[key] = value
        return description

    @staticmethod
    def _put_description(storage, data):
        response = storage
        for key, value in data.items():
            response[key] = value
        return response

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
        f = (version[0:3])[::-1].lstrip('0')
        s = (version[3:5])[::-1].lstrip('0')
        year = (version[5:9])[::-1]
        t = (version[9:])[::-1]
        version = ''.join([t[0], '.', t[1:], '-', year, '.', s, '-', f])
        return version

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
    def _create_item(self, item_info, meta_info, info_parent=None, content_parent=None, position=0):
        version = meta_info['format']

        item_type = item_info['type'] if item_info['type'] in self._stable_types else 'task'
        info_item = InfoStudyItem.objects.create(item_type=item_type, minimal_plugin_version=version,
                                                 parent=info_parent)

        description = Description.objects.create(data=self._get_description(item_info),
                                                 human_language=meta_info['language'])

        if 'course_files' in item_info:
            file = File.objects.create(programming_language=meta_info['programming_language'],
                                       data=item_info['course_files'])
        elif 'task_files' in item_info:
            item_data = {'task_files': item_info['task_files'], 'test_files': item_info['test_files']}
            file = File.objects.create(programming_language=meta_info['programming_language'],
                                       data=item_data)
        else:
            file = None

        content_item = ContentStudyItem.objects.create(info_study_item=info_item, item_type=item_type, file=file,
                                                       description=description, minimal_plugin_version=version)

        if content_parent is not None:
            ContentStudyItemsRelation.objects.create(parent=content_parent, child=content_item, child_position=position)

        response = {'id': info_item.id}
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
            content_child.description.data = self._get_description(new_data=item_info,
                                                                   old_data=content_child.description.data)
            content_child.description.save()

            if 'course_files' in item_info:
                content_child.file.data = item_info['course_files']
                content_child.file.save()

            return content_child

        relation = ContentStudyItemsRelation.objects.get(parent_id=content_parent.id, child_id=content_child.id)

        if relation.is_new and relation.child.item_type != 'task':
            relation.child_position = position
            relation.save()

            content_child.description.data = self._get_description(new_data=item_info,
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
            description = self._get_description(new_data=item_info, old_data=content_child.description.data)
            description = Description.objects.create(data=description, human_language=meta_info['language'])

            item_type = item_info['type'] if 'type' in item_info else content_child.item_type
            if item_type not in self._stable_types:
                item_type = 'task'

            new_content_item = ContentStudyItem.objects.create(info_study_item=info_item, item_type=item_type,
                                                               description=description, minimal_plugin_version=version)
            if 'course_files' in item_info:
                new_content_item.file = File.objects.create(data=item_info['course_files'])
            elif info_item.item_type == 'course':
                new_content_item.file = content_child.file
                new_content_item.save()

            if info_item.item_type == 'task':
                if 'task_files' not in item_info and 'test_files' not in item_info:
                    new_content_item.file = content_child.file
                    new_content_item.save()
                else:
                    current_data = content_child.file.data
                    if 'task_files' in item_info:
                        current_data['task_files'] = item_info['task_files']

                    if 'test_files' in item_info:
                        current_data['test_files'] = item_info['test_files']

                    new_content_item.file = File.objects.create(data=current_data)

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
    def get_all_courses_info(self, suitable_version=None):
        response = {'courses': list()}
        courses = InfoStudyItem.objects.filter(item_type='course')

        for course in courses:
            if suitable_version is not None and compare(course.minimal_plugin_version, suitable_version) > 0:
                continue

            course_version = course.contentstudyitem_set.order_by('-updated_at')
            if suitable_version is not None:
                suitable_course_version = None
                for current_course_version in course_version:
                    if compare(current_course_version.minimal_plugin_version, suitable_version) <= 0:
                        if suitable_course_version is None:
                            suitable_course_version = current_course_version
                        elif compare(suitable_course_version, current_course_version.minimal_plugin_version) < 0:
                            suitable_course_version = current_course_version.minimal_plugin_version
                course_version = suitable_course_version

            if isinstance(course_version, QuerySet):
                course_version = course_version.first()

            minimal_version = course.minimal_plugin_version
            course_info = {'id': course.id, 'format': minimal_version}
            course_info = self._put_description(storage=course_info, data=course_version.description.data)
            response['courses'].append(course_info)
        return response

    def _get_content_item(self, item):
        response = {'id': item.info_study_item.id}
        if item.item_type == 'task':
            response['version_id'] = item.id

        response = self._put_description(storage=response, data=item.description.data)

        if item.item_type == 'course':
            response['last_modified'] = str(item.updated_at)
            response['course_files'] = item.file.data
        elif item.item_type == 'task':
            files = item.file.data
            response['task_files'] = files['task_files']
            response['test_files'] = files['test_files']

        if item.item_type != 'task':
            # now there are two SELECTs every time
            # mb need to change into one INNER JOIN
            subitems = ContentStudyItemsRelation.objects.filter(parent_id=item.id).values_list('child_id',
                                                                                               'child_position')

            ids = [item_id for item_id, position in subitems]
            id_position = dict(subitems)
            subitems = ContentStudyItem.objects.filter(id__in=ids)
            response['items'] = [0] * len(subitems)
            for subitem in subitems:
                response['items'][id_position[subitem.id]] = self._get_content_item(subitem)

        return response

    def get_delta_content_item(self, item, is_new):
        response = {'id': item.info_study_item.id}
        if item.item_type == 'task':
            response['version_id'] = item.id

        if not is_new:
            return response

        response = self._put_description(storage=response, data=item.description.data)
        if item.item_type == 'course':
            response['last_modified'] = str(item.updated_at)

        if item.item_type != 'task':
            # now there are two SELECTs every time
            # mb need to change into one INNER JOIN
            subitems = ContentStudyItemsRelation.objects.filter(parent_id=item.id).values_list('child_id',
                                                                                               'child_position',
                                                                                               'is_new')
            ids = [item_id for item_id, position, is_new in subitems]
            is_new = [is_new for item_id, position, is_new in subitems]
            id_position = dict([(item_id, position) for item_id, position, is_new in subitems])
            subitems = ContentStudyItem.objects.filter(id__in=ids)
            response['items'] = [0] * len(subitems)
            for pos, subitem in enumerate(subitems):
                response['items'][id_position[subitem.id]] = self.get_delta_content_item(subitem, is_new[pos])

        return response

    def check_item(self, item_id, item_type):
        """
        :param item_id: id from httprequest
        :param item_type: type from httprequest
        :return: (result, http_code)
        result can be None
        current http-codes:
        200 - everything is OK,
        404 - there is no item with such id,
        409 - item type with such id is not the same as in httprequest
        """

        try:
            item = InfoStudyItem.objects.get(id=item_id)
        except models.ObjectDoesNotExist:
            return None, 404
        if item.item_type != item_type:
            return None, 409

        content_item = item.contentstudyitem_set.all().order_by('-updated_at').first()
        return self._get_content_item(content_item), 200

    def check_several_items(self, item_id_list, items_type):
        field = items_type + 's'
        response = {field: list()}
        for item_id in item_id_list:
            current_response = self.check_item(item_id, items_type)
            if current_response[1] == 200:
                response[field].append(current_response[0])
            else:
                return current_response
        return response, 200
