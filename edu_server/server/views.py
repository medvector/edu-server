from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from server.course_managers import CourseWriter, CourseGetter


@csrf_exempt
def delete(request):
    course_manager = CourseWriter()
    course_manager._clean_database()
    return HttpResponse(status=200)


@csrf_exempt
def get_or_post(request, version=None, *args, **kwargs):
    if request.method == 'POST':
        course_manager = CourseWriter()
        response = course_manager.create_course(data=request.body)
        return _create_answer(response)
    elif request.method == 'GET':
        course_manager = CourseGetter()
        response = course_manager.get_all_courses_info(suitable_version=version)
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')

    return HttpResponse(status=400)


@csrf_exempt
def update_course(request, course_id, *args, **kwargs):
    course_getter = CourseGetter()
    item, code = course_getter.check_item(course_id, 'course')

    if code != 200:
        return HttpResponse(status=code)
    course_writer = CourseWriter()
    response = course_writer.update_course(data=request.body, course_id=course_id)
    return _create_answer(response=(response, 200))


def _create_answer(response):
    if isinstance(response[0], dict):
        return HttpResponse(content=json.dumps(response[0]), status=response[1], content_type='application/json')
    else:
        return HttpResponse(status=response[1])


def _split_to_numbers(url):
    numbers = [int(number) for number in url.split('&')]
    return numbers


def _get_items(item_id_list, item_type):
    item_id_list = _split_to_numbers(item_id_list)
    course_manager = CourseGetter()
    response = course_manager.check_several_items(item_id_list=item_id_list, items_type=item_type)
    return _create_answer(response)


def get_tasks(request, task_id_list, *args, **kwargs):
    return _get_items(item_id_list=task_id_list, item_type='task')


def get_sections(request, section_id_list, *args, **kwargs):
    return _get_items(item_id_list=section_id_list, item_type='section')


def get_lessons(request, lesson_id_list, *args, **kwargs):
    return _get_items(item_id_list=lesson_id_list, item_type='lesson')


def get_course(request, course_id, version, *args, **kwargs):
    if request.method == 'GET':
        course_manager = CourseGetter()
        item, code = course_manager.check_item(info_item_id=course_id, info_item_type='course', version=version)
        if item is not None:
            item = course_manager._get_content_item(item)
        return _create_answer(response=(item, code))
    else:
        return HttpResponse(status=400)


def get_or_head(request, course_id, version=None):
    course_manager = CourseGetter()
    course, code = course_manager.check_item(course_id, 'course', version)

    if request.method == 'GET':
        course_manager = CourseGetter()
        course, code = course_manager.check_item(course_id, 'course', version)

        if course is not None:
            course = course_manager.get_content_item_delta(content_item=course)

        return _create_answer(response=(course, code))
    elif request.method == 'HEAD' and code == 200:
        response = HttpResponse(status=code)
        response.setdefault(key='Last-Modified', value=str(course.updated_at))
        return response

    return HttpResponse(status=404)


def authorized(request):
    print(request.body.decode('utf-8'))
    print(request.method)
    print(request.path)
    print(request.META)
    print(request.build_absolute_uri())
    print(request.get_full_path())
    print(request.GET.get('token_type'))
    print(request.GET.get('access_token'))
    print(request.GET.get('expires_in'))
    print(request.GET.get('scope'))
    print(request.GET.get('state'))
    return HttpResponse(status=200)


@csrf_exempt
def auth(request):
    ref = 'https://hub.jetbrains.com/api/rest/oauth2/auth?response_type=token&state=9b8fdea0-fc3a-410c-9577-5dee1ae028da&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauthorized&request_credentials=default&client_id=33194796-6023-43b3-8b39-784debb2a646&scope=35b4c62f-a8b2-4ba2-802c-e9f28d4da3be'

    print(request.body.decode('utf-8'))
    print(request.method)
    print(request.path)
    print(request.META)
    return HttpResponseRedirect(ref)