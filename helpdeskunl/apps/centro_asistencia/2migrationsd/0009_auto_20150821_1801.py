# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0008_auto_20150821_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='tiempo_maximo',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='tiempo_normal',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
