# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0007_auto_20150821_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='tiempo_minimo',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
