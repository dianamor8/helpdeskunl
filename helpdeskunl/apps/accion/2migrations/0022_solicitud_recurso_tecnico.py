# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accion', '0021_remove_solicitud_recurso_tecnico'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_recurso',
            name='tecnico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
