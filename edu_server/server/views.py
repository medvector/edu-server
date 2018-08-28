from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from urllib.error import HTTPError
import urllib.request
import base64
import json
from server.course_managers import CourseWriter, CourseGetter
from edu_server import settings
from edu_server.secret_settings import service_id, service_secret
from .user_manager import UserManager


def need_authorization(function_to_decorate):
    def decorated_function(request, *args, **kwargs):
        user_manager = UserManager()
        try:
            is_authorized = user_manager.check_user_authorization(request.META['HTTP_AUTHORIZATION'])
        except (KeyError, ValueError):
            return HttpResponse(status=400)

        if not is_authorized:
            return HttpResponse(status=401)

        return function_to_decorate(request, args, kwargs)

    return decorated_function


@csrf_exempt
def delete(request):
    course_manager = CourseWriter()
    course_manager._clean_database()
    return HttpResponse(status=200)


def _get_all_courses_info(request, version=None):
    course_manager = CourseGetter()
    response = course_manager.get_all_courses_info(suitable_version=version)
    return HttpResponse(json.dumps(response), status=200, content_type='application/json')


def _post_new_course(request):
    course_manager = CourseWriter()
    response = course_manager.create_course(data=request.body)
    return _create_answer(response)


@csrf_exempt
def get_or_post(request, version=None, *args, **kwargs):
    if request.method == 'POST':
        return _post_new_course(request)
    elif request.method == 'GET':
        return _get_all_courses_info(request, version=version)

    return HttpResponse(status=405)


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


def get_course(request, course_id, version=None, *args, **kwargs):
    if request.method == 'GET':
        course_manager = CourseGetter()
        item, code = course_manager.check_item(info_item_id=course_id, info_item_type='course', version=version)
        if item is not None:
            # item = course_manager._get_content_item(item)
            item = course_manager._get_subtree(item)
        return _create_answer(response=(item, code))
    else:
        return HttpResponse(status=405)


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

    return HttpResponse(status=405)


def authorized(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        state = request.GET.get('state')

        if state != settings.HUB_DEFAULT_STATE:
            return HttpResponse(status=400)

        req = urllib.request.Request(settings.HUB_OAUTH_API_BASE_URL + '/token', method='POST')
        grant = 'grant_type=authorization_code&code=' + code + '&redirect_uri=' + settings.DEFAULT_REDIRECT_URI
        req.data = grant.encode()
        req.add_header('Host', 'hub.jetbrains.com')
        req.add_header('Accept', 'application/json')
        service_info = service_id + ':' + service_secret
        b64_service_info = base64.b64encode(service_info.encode('utf-8')).decode()
        req.add_header("Authorization", "Basic %s" % b64_service_info)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')

        try:
            resp = urllib.request.urlopen(req)
        except HTTPError:
            return HttpResponse(status=400)

        tokens_info = json.loads(resp.read().decode('utf-8'))

        req = urllib.request.Request(settings.HUB_REST_API_BASE_URL + '/users/me', method='GET')
        req.add_header('Host', 'hub.jetbrains.com')
        req.add_header('Authorization', "Bearer %s" % tokens_info['access_token'])
        resp = urllib.request.urlopen(req)
        hub_user_info = json.loads(resp.read().decode('utf-8'))

        user_manager = UserManager()
        user = user_manager.check_user_by_hub_id(hub_id=hub_user_info['id'])
        if user is not None:
            user = user_manager.update_user(user, tokens_info, hub_user_info)
        else:
            user = user_manager.create_user(tokens_info, hub_user_info)

        response_data = {'token_type': user.token_type,
                         'access_token': str(user.id) + '.' + user.access_token,
                         'expires_in': str(user.expires_in)}

        return HttpResponse(content=json.dumps(response_data), status=200, content_type='application/json')

    return HttpResponse(status=405)


@csrf_exempt
def auth(request):
    if request.method == 'POST':
        response_type = 'response_type=code'
        state = 'state=' + settings.HUB_DEFAULT_STATE
        redirect_uri = 'redirect_uri=' + settings.DEFAULT_REDIRECT_URI
        request_credentials = 'request_credentials=default'
        client_id = 'client_id=' + service_id
        scope = 'scope=' + settings.HUB_DEFAULT_SCOPE
        access_type = 'access_type=offline'

        args = '&'.join([response_type, state, redirect_uri, request_credentials, client_id, scope, access_type])
        ref = settings.HUB_OAUTH_API_BASE_URL + '/auth?' + args

        return HttpResponseRedirect(ref)

    return HttpResponse(status=405)


@csrf_exempt
@need_authorization
def logout(request):
    user_manager = UserManager()
    user_manager.user_logout(request.META.get('HTTP_AUTHORIZATION'))
    return HttpResponse(status=200)
