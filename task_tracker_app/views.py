from django.shortcuts import render
from .models import Task,Type
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from random import choice as ch

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
            author = User.objects.get(username=params['username'])
        else:
            author = None
        type = Type.objects.get(name_type=params['type'])
        task = Task.objects.create(base_task_id=base_task_id, name_task=name_task, type=type,author=author)
        task.save()
        message = 'Задание успешно добавлено!'
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
        message = 'Задание успешно добавлено!'
    except KeyError:
        message = 'Вы ввели некоретные данные:('

    return render(request, 'message.html', {'message': message})

# привязка таска к пользователю
def task_to_user(request):
    params= request.GET.dict()
    try:
        user_name = User.objects.get(username=params['username'])
        id = params['id']
        Task.objects.filter(id=id).update(author=user_name)
        message = 'Задание успешно привязано к пользователю ' + user_name.username
    except KeyError:
        message = 'Вы ввели некоретные данные:('


    return render(request, 'message.html', {'message': message})

# смена статуса таска
def change_status(request):
    try:
        id = request.GET.dict()['id']
        status = request.GET.dict()['status']
        Task.objects.filter(id=id).update(status=status)
        status_id = int(Task.objects.get(id=id).status)

        if status_id == 1:
            status_name = 'Новая'
        elif status_id == 2:
            status_name = 'В работе'
        elif status_id == 3:
            status_name = 'Выполнено'

        name_task = Task.objects.get(id=id).name_task
        message = 'Статус задачи {} успешно сменён на {}'.format(name_task,status_name)
    except KeyError:
        message = 'Вы ввели некоретные данные:('
    return render(request, 'message.html', {'message': message})


# поиск таска по id, части заголовка. параметры поиска передавать как get параметры запроса
def find_task(request):
    params = request.GET.dict()
    try:
        if 'id' in params:
            id = params['id']
            tasks = Task.objects.filter(id=id)
        elif 'name' in params:
            name = params['name']
            tasks = Task.objects.filter(name_task__contains=name)

    except ObjectDoesNotExist:
        message = 'Такого id не существует:('
        return render(request, 'message.html', {'message': message})

    return render(request, 'task_id.html', {'tasks' : tasks})


# получение всех тасков пользователя ( по id пользователя )
def find_users_task_list(request):

    id = request.GET.dict()['id']
    tasks = Task.objects.filter(author=id)

    return render(request, 'users_task_list.html', {'tasks': tasks})


# получение списка таска с вложенными подтасками
def get_all_tasks(request):

    base_tasks = Task.objects.filter(base_task_id=None)

    tasks_dict = {}

    for base_task in base_tasks:
        tasks_in = Task.objects.filter(base_task_id=base_task)
        tasks_dict[base_task] = tasks_in

    return render(request, 'tasks_in.html', {'tasks_dict': tasks_dict})


def filling(request):

    task_types = Type.objects.all()

    users = User.objects.all()
    base_tasks = Task.objects.all()


    # 1 - created 2 - in progress 3 - done
    status = 1

    for i in range(100000):
        type=ch(task_types)
        user = ch(list(users) + [None])

        base_task = ch(list(base_tasks) + [None])

        if type.name_type == 'дом':
            rooms = ['кухню', 'ванную', 'комнату', 'гостинную']
            actions = ['помыть', 'пропылесосить', 'разобрать']
            room = ch(rooms)
            action = ch(actions)

            name = '{} {}'.format(action, room)

        elif type.name_type == 'учёба':
            courses = ['матан', 'супер ЭВМ', 'базы данных', 'АСОИУ', 'философия']
            actions = ['выучить', 'переписать', 'сделать ДЗ']

            action = ch(actions)
            course = ch(courses)

            name = '{} {}'.format(action, course)

        elif type.name_type == 'работа':
            work = ['составить отчёт', 'сделать задание', 'провести планёрку', 'написать заявление']
            name = ch(work)

        task = Task.objects.create(base_task_id=base_task, name_task=name, type=type, author=user)
        task.save()

    return get_all_tasks(request)

