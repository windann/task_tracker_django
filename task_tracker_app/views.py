from django.shortcuts import render
from .models import Task,Type
from django.contrib import auth

from django.core.exceptions import ObjectDoesNotExist
from random import choice as ch

from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json

def test(request):
    type = Type.objects.all().values()
    return JsonResponse(list(type),safe=False)


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
        tasks = Task.objects\
            .get(id=id).values()
        return JsonResponse(list(tasks),safe=False)
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

        tasks = Task.objects.get(id=id).values()
        return JsonResponse(list(tasks), safe=False)

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

        task = Task.objects.filter(id=id).values()
        return JsonResponse(list(task), safe=False)

    except KeyError:
        message = 'Вы ввели некоретные данные:('

    return render(request, 'message.html', {'message': message})


# смена статуса таска
def change_status(request):
    try:
        id = request.GET.dict()['id']
        status = request.GET.dict()['status']
        Task.objects.filter(id=id).update(status=status)
        task = Task.objects.filter(id=id).values()

        return JsonResponse(list(task), safe=False)

    except KeyError:
        message = 'Вы ввели некоретные данные:('
    return render(request, 'message.html', {'message': message})


# поиск таска по id, части заголовка. параметры поиска передавать как get параметры запроса
def find_task(request):
    params = request.GET.dict()
    try:
        if 'id' in params:
            id = params['id']
            tasks = Task.objects.filter(id=id).values()
        elif 'name' in params:
            name = params['name']
            tasks = Task.objects.filter(name_task__contains=name).values()

        return JsonResponse(list(tasks), safe=False)

    except ObjectDoesNotExist:
        message = 'Такого id не существует:('
        return render(request, 'message.html', {'message': message})



# получение всех тасков пользователя ( по id пользователя )
def find_users_task_list(request):

    id = request.GET.dict()['id']
    tasks = Task.objects.filter(author=id).values()

    return JsonResponse(list(tasks), safe=False)


# получение списка таска с вложенными подтасками
def get_task(request):
    params = request.GET.dict()
    base_task_id = params['id']

    task = Task.objects.filter(id=base_task_id).select_related('author').values()

    #user_id = task[0].author.id
    #author = auth.get_user_model().objects.filter(id=user_id).values()

    #base_task_id = task[0].base_task_id
    #childrens = Task.objects.filter(base_task_id=base_task_id).values()

    #task = dict(task)

    return JsonResponse(list(task), safe=False)

