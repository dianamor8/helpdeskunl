# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0020_auto_20150926_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud_recurso',
            name='tecnico',
        ),
    ]
