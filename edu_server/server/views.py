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
        response = StudyItem.objects.create_course(course_data=request.body)
        return HttpResponse(json.dumps(response), status=201, content_type='application/json')
    elif request.method == 'GET':
        response = StudyItem.objects.get_all_courses
        return HttpResponse(json.dumps(response), status=200, content_type='application/json')

    return HttpResponse(status=200)


@csrf_exempt
def update_course(request, id=0, *args, **kwargs):
    print(id)
    return HttpResponse(status=404)