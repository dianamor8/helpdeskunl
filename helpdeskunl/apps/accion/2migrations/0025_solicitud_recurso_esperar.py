# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0024_solicitud_recurso_notificar_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_recurso',
            name='esperar',
            field=models.BooleanField(default=True),
        ),
    ]
