# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problema', '0001_initial'),
        ('accion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accion',
            name='problema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='problema.Problema', null=True),
        ),
        migrations.AddField(
            model_name='accion',
            name='solicitud_recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='accion.Solicitud_Recurso', null=True),
        ),
        migrations.AddField(
            model_name='accion',
            name='tecnico',
            field=models.ForeignKey(related_name='tecnico', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
