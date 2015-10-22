# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_perfil_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='activo',
            field=models.BooleanField(default=True, verbose_name=b'Usuario activo'),
            preserve_default=True,
        ),
    ]
