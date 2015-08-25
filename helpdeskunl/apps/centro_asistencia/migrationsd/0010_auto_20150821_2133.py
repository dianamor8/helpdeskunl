# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timedelta.fields


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0009_auto_20150821_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='tiempo_maximo',
            field=timedelta.fields.TimedeltaField(),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='tiempo_minimo',
            field=timedelta.fields.TimedeltaField(),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='tiempo_normal',
            field=timedelta.fields.TimedeltaField(),
        ),
    ]
