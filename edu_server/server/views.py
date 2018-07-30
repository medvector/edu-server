from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from server.models import CourseManager


@csrf_exempt
def get_or_post(request, version=None, *args, **kwargs):
    course_manager = CourseManager()
    if request.method == 'POST':
        response = course_manager.create_course(data=request.body)
        return HttpResponse(json.dumps(response), status=201, content_type='application/json')
    elif request.method == 'GET':
        response = course_manager.get_all_courses_info(version=version)
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')

    return HttpResponse(status=400)


@csrf_exempt
def update_course(request, course_id, *args, **kwargs):
    course_manager = CourseManager()
    response = course_manager.update_course(data=request.body, course_id=course_id)
    return _create_answer(response=response)


def _create_answer(response):
    if isinstance(response, dict):
        return HttpResponse(content=json.dumps(response), status=200, content_type='application/json')
    else:
        return HttpResponse(status=response)


def _split_to_numbers(url):
    numbers = [int(number) for number in url.split('&')]
    return numbers


def _get_items(item_id_list, item_type):
    item_id_list = _split_to_numbers(item_id_list)
    course_manager = CourseManager()
    response = course_manager._check_several_hidden_items(item_id_list=item_id_list, items_type=item_type)
    return _create_answer(response)


def get_tasks(request, task_id_list, *args, **kwargs):
    return _get_items(item_id_list=task_id_list, item_type='task')


def get_sections(request, section_id_list, *args, **kwargs):
    return _get_items(item_id_list=section_id_list, item_type='section')


def get_lessons(request, lesson_id_list, *args, **kwargs):
    return _get_items(item_id_list=lesson_id_list, item_type='lesson')


def get_course(request, course_id, *args, **kwargs):
    course_manager = CourseManager()
    response = course_manager._check_hidden_item(item_id=course_id, item_type='course')
    return _create_answer(response=response)