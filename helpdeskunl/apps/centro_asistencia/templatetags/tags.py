# -*- coding: utf-8 -*-
from django import template
from helpdeskunl.apps.centro_asistencia.forms import *
from datetime import timedelta

register = template.Library()

# @register.inclusion_tag('centro_asistencia/form_agregar_centro_asistencia_html.html', takes_context=True)
# def agregar_centro_asistencia(context, pk=None):
# 	form = form_agregar_centro_asistencia()
# 	# if pk is not None:		
# 		# categoria = Categoria.objects.filter(id=pk)
# 		# if categoria:
# 		# 	categoria = Categoria.objects.get(id=pk)		 	
# 		# 	form = addCategoriaForm(instance=categoria)		
# 		# agregar aqui la clave foranea	
# 	contexto = {'form_agregar_centro_asistencia': form}
# 	return contexto


def timedeltaformat(value):
	if value.days == 1:	
		return str(value).replace(" day, ", " DIA, ")

	if value.days > 1:	
		return str(value).replace(" days, ", " DIAS, ")
	return value

register.filter('timedeltaformat',timedeltaformat)
