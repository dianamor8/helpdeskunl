# HTTP
from django.http import HttpResponse
from django.shortcuts import render
# PROYECTO
from helpdeskunl.apps.usuarios.models import *
import json
from django.core import serializers

def buscar_usuarios(request):
	if request.is_ajax():
		try:
			campo = request.GET['campo']
			valor = request.GET['valor']
			if campo == 'dni':			
				users = Perfil.objects.filter(dni__startswith=valor).only('dni', 'nombres', 'apellidos', 'departamento').distinct().order_by(campo)
				usuarios = list()		
				for u in users:	
					usuarios.append({'dni':u.dni, 'nombres': u.nombres, 'apellidos' : u.apellidos, 'departamento': u.departamento})
			if campo == 'nombres':			
				users = Perfil.objects.filter(nombres__istartswith=valor).values('dni', 'nombres', 'apellidos', 'departamento').distinct().order_by('nombres', 'apellidos')
				usuarios = list(users)	
			if campo == 'apellidos':			
				users = Perfil.objects.filter(apellidos__istartswith=valor).values('dni', 'nombres', 'apellidos', 'departamento')
				users.distinct().order_by('apellidos','nombres')
				usuarios = list(users)	

			# print "======="
			# print users.query
			# print "======="

			# if len(users)>0:
			# 	users.distinct().order_by(campo)				
			
			# print users
			# usuarios_html = list()
			# usuarios = list(users)		
			# for u in users:					
			# 	# usuarios_html.append({'tabla':'<tr><td>%s</td><td>%s %s</td><td>%s</td></tr>'%(u.dni, u.nombres,u.apellidos,u.departamento),})				
			# 	usuarios.append({'dni':u.dni, 'nombres_completos': u.nombres + ' ' + u.apellidos, 'departamento': u.departamento})
			# # ctx={'tabla':usuarios_html}

			ctx={'usuarios':usuarios}

			# datos = serializers.serialize('json',users,fields('dni','nombres','apellidos','departamento'))
			return HttpResponse(json.dumps(ctx), content_type='application/json') 
		except Exception, e:		
			ctx = {'message':e}
			return HttpResponse(json.dumps(ctx), content_type='application/json') 
	else:
		return render(request, 'usuario/buscar_usuarios.html')

	