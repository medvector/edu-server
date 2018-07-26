from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from server.models import StudyItem
import json


# Create your views here.


@csrf_exempt
def get_or_post(request, *args, **kwargs):
    if request.method == 'POST':
        response = StudyItem.objects.create_course(data=request.body)
        return HttpResponse(json.dumps(response), status=201, content_type='application/json')
    elif request.method == 'GET':
        response = StudyItem.objects.get_all_courses_info
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')

    return HttpResponse(status=200)


@csrf_exempt
def update_course(request, course_id=0, *args, **kwargs):
    print(course_id)
    return HttpResponse(status=404)


def create_answer(response, item_type):
    code = 200
    for item in response[item_type + 's']:
        if not isinstance(item, dict):
            if code != item and code == 200:
                code = item
            else:
                code = 400

    if code == 200:
        return HttpResponse(content=json.dumps(response), status=code, content_type='application/json')
    else:
        return HttpResponse(status=code)


def _split_to_numbers(url):
    numbers = [int(number) for number in url.split('&')]
    return numbers


def _get_items(item_id_list, item_type):
    item_id_list = _split_to_numbers(item_id_list)
    response = StudyItem.objects._get_items(item_id_list=item_id_list, item_type=item_type)
    return response


def get_tasks(request, task_id_list, *args, **kwargs):
    response = _get_items(item_id_list=task_id_list, item_type='task')
    return create_answer(response=response, item_type='task')


def get_sections(request, section_id_list, *args, **kwargs):
    response = _get_items(item_id_list=section_id_list, item_type='section')
    return create_answer(response=response, item_type='section')


def get_lessons(request, lesson_id_list, *args, **kwargs):
    response = _get_items(item_id_list=lesson_id_list, item_type='lesson')
    return create_answer(response=response, item_type='lesson')


def get_course(request, course_id, *args, **kwargs):
    response = StudyItem.objects.get_course(course_id=course_id)
    if isinstance(response, dict):
        return HttpResponse(content=json.dumps(response), status=200, content_type='application/json')
    else:
        return HttpResponse(status=response)
