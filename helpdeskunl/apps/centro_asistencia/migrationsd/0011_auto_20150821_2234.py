# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0010_auto_20150821_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio',
            name='tiempo_maximo',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='tiempo_minimo',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='tiempo_normal',
        ),
        migrations.AddField(
            model_name='servicio',
            name='time_passed',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
