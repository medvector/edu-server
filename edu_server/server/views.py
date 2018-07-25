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


def create_answer(response):
    if isinstance(response, dict):
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')
    elif response == 404:
        return HttpResponse('Not Found', status=response, content_type='text/plain')
    elif response == 409:
        return HttpResponse('Conflict', status=response, content_type='text/plain')


def get_task(request, task_id, *args, **kwargs):
    response = StudyItem.objects.get_task(task_id=task_id)
    return create_answer(response=response)


def get_section(request, section_id, *args, **kwargs):
    response = StudyItem.objects.get_section(section_id=section_id)
    return create_answer(response=response)


def get_lesson(request, lesson_id, *args, **kwargs):
    response = StudyItem.objects.get_lesson(lesson_id=lesson_id)
    return create_answer(response=response)


def get_course(request, course_id, *args, **kwargs):
    response = StudyItem.objects.get_course(course_id=course_id)
    return create_answer(response=response)