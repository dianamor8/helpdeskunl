 # -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

# HELPDESK
from helpdeskunl.apps.centro_asistencia.forms import *
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *

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

##########
#AGREGAR USUARIOS ADMINISTRADORES O JEFES DE DEPARTAMENTO AL CENTRO DE ASISTENCIA 
##########
@login_required
@permission_required('centro_asistencia.add_personal_operativo',raise_exception=True)
def agregar_usuario(request):
	if  request.method == 'POST':
		# SE ALMACENA EL DATO DE LA APP QUE LLAMA A LA VENTANA BUSCAR USUARIO
		app = request.POST.get('app')
		if app == 'centro_asistencia':
			name_group = request.POST.get('tipo_usuario')
			dni_usuario = request.POST.get('usuario')
			pk_centro_asistencia = request.POST.get('centro_asistencia')			
			usuario = Perfil.objects.get(dni = dni_usuario)
			centro = Centro_Asistencia.objects.get(pk= pk_centro_asistencia)
			if name_group == 'JEFE DEPARTAMENTO':
				g = Group.objects.get(name='JEFE DEPARTAMENTO')
				centros_asistencia = Centro_Asistencia.objects.administrado_por_mi(user=usuario)
				c = [cen.pk for cen in centros_asistencia]
				if int(pk_centro_asistencia) in c:
					ctx={'respuesta':'ERROR. ', 'mensaje':'Este usuario ya ha sido agregado.'}
					return HttpResponse(json.dumps(ctx), content_type='application/json')		
			elif name_group == 'ASESOR TECNICO':
				g = Group.objects.get(name='ASESOR TECNICO')
				centros_asistencia = Centro_Asistencia.objects.acesorado_por_mi(user=usuario)
				c = [cen.pk for cen in centros_asistencia]
				if int(pk_centro_asistencia) in c:
					ctx={'respuesta':'ERROR. ', 'mensaje':'Este usuario ya ha sido agregado.'}
					return HttpResponse(json.dumps(ctx), content_type='application/json')
			# AGREGO EL USUARIO AL GRUPO 
			g.user_set.add(usuario)
			personal = Personal_Operativo(centro_asistencia= centro, usuario=usuario, grupo = g)			
			personal.save()
			contexto ={'respuesta': 'OK. ', 'mensaje': 'El usuario se agregó con éxito.'}				
			return HttpResponse(json.dumps(contexto), content_type='application/json')				
			# return redirect('/centro_asistencia/'+pk_centro_asistencia+'/', contexto)
	else:
		raise Http404


@login_required
@permission_required('centro_asistencia.delete_personal_operativo',raise_exception=True)
def eliminar_usuario(request):
	print 'entrando'	
	if request.method == 'POST':		
		try:
			name_group = request.POST.get('tipo_usuario')
			dni_usuario = request.POST.get('dni')
			pk_centro_asistencia = request.POST.get('centro_asistencia')
			if name_group == 'JEFE DEPARTAMENTO':
				grupo = Group.objects.get(name='JEFE DEPARTAMENTO')
				bandera = True #PARA SABER SI SE ESTA AUTOELIMINANDO EN JEFE DEPARTAMENTO
			elif name_group == 'ASESOR TECNICO':
				grupo = Group.objects.get(name='ASESOR TECNICO')
				bandera = False		
			usuario = Perfil.objects.get(dni = dni_usuario)			
			if (usuario == request.user) and bandera:
					ctx={'respuesta':'ERROR. ', 'mensaje':'No es posible realizar una autoeliminación de datos. Contacte con el administrador.'}
					return HttpResponse(json.dumps(ctx), content_type='application/json')
			else:	
				centro_asistencia = Centro_Asistencia.objects.filter(id=pk_centro_asistencia)
				personal = Personal_Operativo.objects.filter(usuario=usuario, centro_asistencia=centro_asistencia, grupo=grupo)
				personal.delete()
				# VERIFICAR SI ESTE USUARIO EXISTE FORMA PARTE DE OTRO CENTRO DE ASISTENCIA CON EL MISMO GRUPO
				personal_aux= Personal_Operativo.objects.filter(usuario=usuario, grupo=grupo)

				if not personal_aux:
					# SE LE QUITA LOS PERMISOS
					grupo.user_set.remove(usuario)
				ctx={'respuesta':'OK. ', 'mensaje':'Se ha eliminado exitosamente.'}
				return HttpResponse(json.dumps(ctx), content_type='application/json')
		except Exception, e:
			print e
			ctx={'respuesta':'ERROR. ', 'mensaje':'Hubo un error al eliminar.'}
			return HttpResponse(json.dumps(ctx), content_type='application/json')
	else:
		raise Http404