# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('centro_asistencia', '0006_auto_20150821_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='tiempo_maximo',
            field=models.DurationField(default=datetime.datetime(2015, 8, 21, 17, 35, 57, 364231, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicio',
            name='tiempo_normal',
            field=models.DurationField(default=datetime.datetime(2015, 8, 21, 17, 36, 11, 713646, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
