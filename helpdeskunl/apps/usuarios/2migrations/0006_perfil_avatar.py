# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import helpdeskunl.apps.usuarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_auto_20150821_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='avatar',
            field=models.ImageField(help_text=b'Seleccione una imagen.', max_length=300, null=True, upload_to='', blank=True),
        ),
    ]
