from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from server.models import StudyItem
import json
# Create your views here.


@csrf_exempt
def get_or_post(request, *args, **kwargs):
    if request.method is 'POST':
        try:
            StudyItem.objects.save_new_course(data=request.body)
        except Exception:
            return HttpResponse(status=400)
        return HttpResponse(status=201, content='Created')
    elif request.method is 'GET':
        return HttpResponse(status=404)


@csrf_exempt
def update_course(request, id=0, *args, **kwargs):
    print(id)
    return HttpResponse(status=404)