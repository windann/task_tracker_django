# Generated by Django 2.0.5 on 2018-05-25 09:01

from django.db import migrations
from django.contrib import auth
from random import choice as ch, random as r
from django.conf import settings
from faker import Faker

from transliterate import translit


def filling_tasks(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Type = apps.get_model('task_tracker_app', "Type")
    Task = apps.get_model('task_tracker_app', "Task")
    User = apps.get_model('auth',"User")

    task_types = Type.objects.all()

    users = User.objects.all()
    base_tasks = Task.objects.all()

    # 1 - created 2 - in progress 3 - done
    status = 1

    for i in range(100000):
        type = ch(task_types)
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

        elif type.name_type == 'покупки':
            products = ['молоко', 'хлеб', 'кефир', 'яблоки', 'шоколад', 'капуста', 'сок']
            product = ch(products)

            name = 'купить {}'.format(product)

        task = Task.objects.create(base_task_id=base_task, name_task=name, type=type, author=user)
        print(task)
        task.save()


def filling_users(apps, schema_editor):
    fake = Faker('ru_RU')
    User = apps.get_model('task_tracker_app', auth.get_user_model())

    for i in range(10000):
        first_name = fake.first_name()
        last_name = fake.last_name()
        login = translit(first_name[:2], reversed=True) + translit(last_name[:2], reversed=True) + str(i)

        u = User.objects.create(first_name=first_name,last_name = last_name,username=login)
        print(u)
        u.save()


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker_app', '0006_auto_20180520_1506'),
    ]

    operations = [
        migrations.RunPython(filling_tasks),
        migrations.RunPython(filling_users)
    ]
