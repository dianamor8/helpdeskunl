# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accion', '0023_solicitud_recurso_en_espera'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_recurso',
            name='notificar_email',
            field=models.BooleanField(default=False),
        ),
    ]
