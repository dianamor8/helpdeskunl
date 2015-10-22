# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0011_auto_20150821_2234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio',
            name='time_passed',
        ),
        migrations.AddField(
            model_name='servicio',
            name='t_maximo',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='t_minimo',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='t_normal',
            field=models.DurationField(null=True, blank=True),
        ),
    ]
