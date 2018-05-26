from django.shortcuts import render
from .models import Task,Type
from django.contrib import auth

from django.core.exceptions import ObjectDoesNotExist
from random import choice as ch

from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json


def type_serialize(types):
    return [{"id":type_name.pk, "name_type":type_name.name_type} for type_name in types]

def task_serialize(task):

    if type(task) != list:

        return {"id":task.pk,"name_task":task.name_task,"status":task.status,
             "author":task.author.username,"type":task.type.name_type,"base_task":task.base_task_id.name_task,
             "date":task.date}

    else:
        return [{"id": elem.pk, "name_task": elem.name_task, "status": elem.status,
                "author": elem.author.username, "type": elem.type.name_type, "base_task": elem.base_task_id.name_task,
                "date": elem.date} for elem in task]

def task_serialize_with_children(task,childrens):

    return {"id":task.pk,"name_task":task.name_task,"status":task.status,
             "author":{"first_name":task.author.first_name,"last_name":task.author.last_name},"type":task.type.name_type,"base_task":task.base_task_id.name_task,
             "date":task.date,"childrens":childrens}


# создание нового таска
def add_new_task(request):
    try:
        params = request.GET.dict()
        name_task = params['name_task']
        if 'id' in params:
            base_task_id = Task.objects.get(id=params['id'])
        else:
            base_task_id = None
        if 'username' in params:
            author = auth.get_user_model().objects.get(username=params['username'])
        else:
            author = None
        type = Type.objects.get(name_type=params['type'])
        task = Task.objects.create(base_task_id=base_task_id, name_task=name_task, type=type,author=author)
        task.save()
        tasks = list(Task.objects.all())[-1]
        return JsonResponse(task_serialize(tasks),safe=False)
    except KeyError:
        message = 'Вы ввели некоретные данные:('
        return render(request, 'message.html', {'message': message})


# создание дочернего таска
def add_task_in(request):
    params = request.GET.dict()
    try:
        base_task_id = Task.objects.get(id=params['id'])
        name_task = params['name_task']
        type = Type.objects.get(name_type=params['type'])
        author = base_task_id.author
        task = Task.objects.create(base_task_id=base_task_id,name_task=name_task,type=type,author=author)
        task.save()

        tasks = list(Task.objects.all())[-1]
        return JsonResponse(task_serialize(tasks), safe=False)

    except KeyError:
        message = 'Вы ввели некоретные данные:('

    return render(request, 'message.html', {'message': message})


# привязка таска к пользователю
def task_to_user(request):
    params= request.GET.dict()
    try:
        user_name = auth.get_user_model().objects.get(username=params['username'])
        id = params['id']

        Task.objects.filter(id=id).update(author=user_name)
        tasks = Task.objects.get(id = id)

        return JsonResponse(task_serialize(tasks), safe=False)

    except KeyError:
        message = 'Вы ввели некоретные данные:('

    return render(request, 'message.html', {'message': message})


# смена статуса таска
def change_status(request):
    params = request.GET.dict()
    try:
        task_id = params['id']
        status = params['status']
        Task.objects.filter(id=task_id).update(status=status)
        tasks = Task.objects.get(id=task_id)
        return JsonResponse(task_serialize(tasks), safe=False)

    except KeyError:
        message = 'Вы ввели некоретные данные:('

    return render(request, 'message.html', {'message': message})


# поиск таска по id, части заголовка. параметры поиска передавать как get параметры запроса
def find_task(request):
    params = request.GET.dict()
    try:

        if 'id' in params:
            id = params['id']
            tasks = Task.objects.get(id=id)

        elif 'name' in params:
            name = params['name']
            tasks = Task.objects.filter(name_task__contains=name)

        return JsonResponse(task_serialize(tasks), safe=False)

    except ObjectDoesNotExist:
        message = 'Такого id не существует:('
        return render(request, 'message.html', {'message': message})


# получение всех тасков пользователя ( по id пользователя )
def find_users_task_list(request):

    id = request.GET.dict()['id']
    tasks = Task.objects.filter(author=id)

    return JsonResponse(task_serialize(tasks), safe=False)


# получение списка таска с вложенными подтасками
def get_task(request):
    params = request.GET.dict()
    task_id = params['id']

    task = list(Task.objects.filter(id=task_id).select_related('author','base_task_id'))[0]
    childrens = [task.name_task for task in Task.objects.filter(base_task_id=task_id)]

    return JsonResponse(task_serialize_with_children(task,childrens), safe=False)

