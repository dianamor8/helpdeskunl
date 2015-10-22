# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('dni', models.CharField(unique=True, max_length=50, verbose_name=b'DNI')),
                ('nombres', models.CharField(max_length=250, verbose_name=b'Nombres')),
                ('apellidos', models.CharField(max_length=250, verbose_name=b'Apellidos')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'Direcci\xc3\xb3n de correo')),
                ('departamento', models.CharField(max_length=350, verbose_name=b'Departamento')),
                ('contacto', models.CharField(max_length=50, verbose_name=b'Contacto')),
                ('tipo', models.CharField(max_length=100, verbose_name=b'Personal', choices=[(b'0', b'Administrativo'), (b'1', b'Docente')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Perfil',
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
            bases=(models.Model,),
        ),
    ]
