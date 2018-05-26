"""task_tracker URL Configuration

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
from django.urls import path
from task_tracker_app.views import find_task, \
    change_status,\
    find_users_task_list,\
    add_task_in,add_new_task,\
    get_task, \
    task_to_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('find_task/', find_task),
    path('change_status/', change_status),
    path('tasks_list/', find_users_task_list),
    path('add_task_in/',add_task_in),
    path('add/',add_new_task),
    path('tasks_in/',get_task),
    path('task_to_user/',task_to_user),
]
