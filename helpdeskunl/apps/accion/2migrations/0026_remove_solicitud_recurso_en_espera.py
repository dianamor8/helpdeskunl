# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0025_solicitud_recurso_esperar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud_recurso',
            name='en_espera',
        ),
    ]
