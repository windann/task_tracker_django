# Generated by Django 2.0.5 on 2018-05-20 15:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker_app', '0004_auto_20180520_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(default=None, on_delete='null', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
