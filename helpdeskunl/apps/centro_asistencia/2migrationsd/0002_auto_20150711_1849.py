# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('centro_asistencia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Centro_Asistencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'Centro_Asistencia',
                'verbose_name': 'Centro de Asistencia',
                'verbose_name_plural': 'Centros de Asistencia',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personal_Operativo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('centro_asistencia', models.ForeignKey(to='centro_asistencia.Centro_Asistencia')),
                ('grupo', models.ForeignKey(to='auth.Group')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Personal_Operativo',
                'verbose_name': 'Personal Operativo',
                'verbose_name_plural': 'Personal Operativo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=250)),
                ('centro', models.ForeignKey(to='centro_asistencia.Centro_Asistencia')),
            ],
            options={
                'db_table': 'Servicio',
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='centro_asistencia',
            name='usuarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='centro_asistencia.Personal_Operativo'),
            preserve_default=True,
        ),
    ]
