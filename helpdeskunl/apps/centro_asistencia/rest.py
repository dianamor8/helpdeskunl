 # -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from helpdeskunl.apps.centro_asistencia.forms import *
@login_required
@permission_required('centro_asistencia.add_centro_asistencia',raise_exception=True)
def centro_asistencia_add_ajax(request):	
	if request.is_ajax():		
		if request.method == 'POST':
			respuesta = False
			form_centro_asistencia = form_agregar_centro_asistencia(request.POST)
			if form_centro_asistencia.is_valid():
				nombre= request.POST.get('nombre')
				centro_existente = Centro_Asistencia.objects.filter(nombre=nombre)
				if not centro_existente:
					form_centro_asistencia.save()
					respuesta = True
					ctx={'respuesta':respuesta}					
				else:
					listaErrores =list()
					listaErrores.append('Ya existe un centro de asistencia con ese nombre.')
					ctx={'respuesta':respuesta, 'errores':listaErrores}				
			else:
				errores = form_centro_asistencia.errors
				ctx={'respuesta':respuesta, 'errores':errores}
		return HttpResponse(json.dumps(ctx), content_type='application/json')		
	else:
		raise Http404		