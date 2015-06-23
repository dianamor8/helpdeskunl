# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='estilo_fondo')
def estilo_fondo(user):

	# AGREGAR UNA FUNCIÓN PARA AUTENTICARSE COMO EL USUARIO DESEE SI TIENE MAS DE UN GRUPO ASIGNADO

	if user.groups.filter(name='JEFE DEPARTAMENTO').exists() or user.groups.filter(name='SUPER ADMINISTRADOR').exists():
		estilo = 'FONDO OSCURO'
	elif user.groups.filter(name='ASESOR TECNICO').exists():
		estilo = 'FONDO CAFE'		
	elif user.groups.filter(name='USUARIO FINAL').exists():
		estilo = 'FONDO VERDE'
	else:
		estilo = 'NINGUNO'	
	return estilo


