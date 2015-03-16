# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0004_auto_20150127_2208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria_equipo',
            options={'verbose_name': 'Categoria del equipo', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='marca_equipo',
            options={'verbose_name': 'Marca', 'verbose_name_plural': 'Marcas'},
        ),
        migrations.AlterField(
            model_name='equipo',
            name='modelo',
            field=models.CharField(max_length=250, null=True),
            preserve_default=True,
        ),
    ]
