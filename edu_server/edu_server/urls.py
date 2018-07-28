"""edu_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from server import views

urlpatterns = [
    # path('courses', views.get_or_post, name='get_or_post'),
    # path('courses/<str:plugin_version>', views.get_or_post, name='get_or_post'),
    # path('courses/<int:course_id>', views.update_course, name='update_course'),
    # path('courses/<int:course_id>/materials', views.get_course, name='get_course'),
    # re_path('sections/((\d+&?)+)', views.get_sections, name='get_sections'),
    # re_path('lessons/((\d+&?)+)', views.get_lessons, name='get_lessons'),
    # re_path('tasks/((\d+&?)+)', views.get_tasks, name='get_tasks'),
]
