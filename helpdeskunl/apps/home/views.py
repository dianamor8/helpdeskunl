# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User, Group

# Create your views here.
# def index_view(request):
# 	if request.user.is_authenticated():
# 		usuario = request.user			
# 		grupos = usuario.groups.values_list('name',flat=True)

# 		if grupos.exists():			
# 			nombre_grupo = ''
# 			for grupo in grupos:			
# 				grupo.encode('utf-8')			
# 				if grupo == u'Jefe Departamento':					
# 					return render(request,'home/home_admin.html')
# 				if grupo == u'Técnico Operativo':
# 					return render(request,'home/home_operativo.html')
# 				if grupo == u'Usuario Final':
# 					return render(request,'home/home_cliente.html')			
# 			return render(request,'home/home_cliente.html')		
# 		else:
# 			print "El usuario aun no ha sido asignado un grupo. CONSULTE AL ADMINISTRADOR"
# 			return render(request,'home/index.html')
# 	else:
# 		return render(request,'home/index.html')

def index_view(request):
	if request.user.is_authenticated():
		usuario = request.user			
		grupos = usuario.groups.values_list('name',flat=True)
		if grupos.exists():			
			# for grupo in grupos:			
			# 	grupo.encode('utf-8')							
			# 	nombre_grupo = grupo;							
			return render(request,'home/home_general.html')		
		else:
			print "El usuario aun no ha sido asignado un grupo. CONSULTE AL ADMINISTRADOR"
			return render(request,'home/index.html')
	else:
		return render(request,'home/index.html')


def panel_view(request, dni):	
	if request.user.is_authenticated():
		usuario = Perfil.objects.get(dni=dni)		
		grupos = usuario.groups.values_list('name',flat=True)
		for grupo in grupos:			
			grupo.encode('utf-8')			
			if grupo == u'JEFE DEPARTAMENTO':
				return render(request,'home/home_admin.html')
			if grupo == u'ASISTENTE TECNICO':
				return render(request,'home/home_operativo.html')
			if grupo == u'USUARIO FINAL':
				return render(request,'home/home_cliente.html')
		return render(request,'home/home_cliente.html')			
	else:
		print 'NO HA INICIADO SESIÓN'
	# si el usuario importar User es admin 
	# return render(request,'home/home_admin.html')
	# si el usuario importar User es operativo
	#return render(request,'home/home_operativo.html')
	# si el usuario importar User es administrativonunl	
	#return render(request,'home/home_cliente.html')


	#Si es usuario admin renderizar el home_admin
	#Si es usuario operador renderizar el home_operador
	#Sie es usuario administrativo renderizar home_administrativo

	# http://django-book.blogspot.com/2012/11/metodos-de-los-modelos-definir-metodos.html
	# http://django.es/blog/metodos-para-crear-perfiles-de-usuario/
	# https://librosweb.es/libro/django_1_0/capitulo_12/utilizando_usuarios.html
	# https://www.youtube.com/watch?v=TO3O38L0YsI
	# http://danyalejandro.com/portafolio/articulos/web-services-php-breve-introduccion
	# https://docs.djangoproject.com/en/1.8/topics/auth/