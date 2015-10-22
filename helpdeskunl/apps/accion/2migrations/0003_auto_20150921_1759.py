# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('home', '__first__'),
        ('accion', '0002_auto_20150921_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_recurso',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='home.Contacto', null=True),
        ),
        migrations.AlterField(
            model_name='accion',
            name='tecnico',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.DO_NOTHING),
        ),
    ]
