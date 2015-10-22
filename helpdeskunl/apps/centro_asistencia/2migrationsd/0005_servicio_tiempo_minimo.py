# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0004_auto_20150806_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='tiempo_minimo',
            field=models.DurationField(default=datetime.datetime(2015, 8, 21, 17, 16, 29, 553753, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
