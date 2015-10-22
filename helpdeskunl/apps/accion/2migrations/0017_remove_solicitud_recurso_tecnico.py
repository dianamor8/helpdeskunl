# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0016_auto_20150926_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud_recurso',
            name='tecnico',
        ),
    ]
