 # -*- coding: utf-8 -*-
import json
from django.core import serializers
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

		# ctx={'duracion': str(incidencia.duracion), 'caduca': str(caducidad),}	
		ctx={'duracion': str(incidencia.duracion),}	
		return HttpResponse(json.dumps(ctx), content_type='application/json')		
	else:
		raise Http404

# BUSCAR BIENES

def buscar_bienes(request):
	print "prueba full path buscar bienes"
	print request.get_full_path()
	if request.is_ajax():
		try:
			campo = request.GET['campo']
			valor = request.GET['valor']			
			if campo == 'codigo':
				try:
				    bien = Bien.objects.get(codigo=valor)				    
				except Bien.DoesNotExist:
					bien = None
			if campo == 'codigo_cfn':			
				try:
					bien = Bien.objects.get(codigo_cfn =valor)
				except Bien.DoesNotExist:
					bien = None
			if campo == 'serie':			
				try:					
					bien = Bien.objects.get(serie =valor)
				except Bien.DoesNotExist:
					bien = None
			
			if bien is None:
				ctx={'bien':'notfound'}				
			else:				
				cadena = '<tr id= "trbien_%s"> <input type="hidden" value="%s" name="bien"> <td>%s</td> <td>%s</td><td>%s</td><td>%s</td><td><input type="button" class="btn btn-danger remover" data-id="%s" value="x"></td></tr>' %(bien.id,bien.id, bien.codigo, bien.codigo_cfn, bien.serie, bien.producto, bien.id)
				ctx={'fila':cadena, 'id': bien.id,}
			return HttpResponse(json.dumps(ctx), content_type='application/json') 
		except Exception, e:		
			ctx = {'message':e}			
			return HttpResponse(json.dumps(ctx), content_type='application/json') 
	else:
		return render(request, request.get_full_path())


@login_required
def cerrar_incidencia_expirada(request):	
	if  request.is_ajax():	
		incidencias = Incidencia.objects.filter(estado=True, estado_incidencia='2', asignacion_incidencia__tecnico=request.user)
		for incidencia in incidencias:			
			variable = incidencia.es_vigente(request)	
		ctx={'realizado': 'si',}	
		return HttpResponse(json.dumps(ctx), content_type='application/json')		
	else:
		raise Http404