# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20150417_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='activo',
            field=models.BooleanField(default=True, verbose_name=b'Usuario UNL activo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name=b'Usuario activo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name=b'Usuario Administrador'),
            preserve_default=True,
        ),
    ]
