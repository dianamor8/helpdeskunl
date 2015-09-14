 # -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

# HELPDESK
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.centro_asistencia.templatetags.tags import *

from django.shortcuts import get_object_or_404
from django.utils import formats




@login_required
def calcular_incidencia_ajax(request):	
	if  request.is_ajax():
		incidencia = get_object_or_404(Incidencia, pk=request.GET.get('incidencia'))		
		incidencia.prioridad_asignada = request.GET.get('p_asignada')				
		incidencia.servicio = get_object_or_404(Servicio, pk=request.GET.get('servicio'))		
		incidencia.ejecucion = incidencia.determinar_prioridad() #fijado p-sol y p-asig			
		incidencia.duracion = incidencia.determinar_duracion() #fijado ejecucion y servicio		
		incidencia.caducidad = incidencia.calcular_caducidad() #fijado fecha y duracion				
		caducidad = formats.date_format(incidencia.calcular_caducidad(), "SHORT_DATE_FORMAT")

		ctx={'duracion': str(incidencia.duracion), 'caduca': str(caducidad),}	
		return HttpResponse(json.dumps(ctx), content_type='application/json')		
	else:
		raise Http404