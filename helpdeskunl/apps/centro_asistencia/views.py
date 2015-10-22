# -*- coding: utf-8 -*-
# HTTP
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.loader import render_to_string
import json
from django.core import serializers
# HELPDESKUNL
from helpdeskunl.settings import LOGIN_URL
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.centro_asistencia.forms import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.centro_asistencia.templatetags.tags import *
# GENERAL
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView,ListView
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.contrib import messages
#METODOS DECORADORES
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
# ERRORES Y EXCEPCIONES
from django.forms.utils import ErrorList
from django.db import IntegrityError

from drealtime import iShoutClient
ishout_client = iShoutClient()

##############################
# MODEL CENTRO DE ASISTENCIA #
##############################



def permiso_requerido(user):
	agregar = user.has_perm('centro_asistencia.add_centro_asistencia')
	actualizar = user.has_perm('centro_asistencia.change_centro_asistencia')
	eliminar = user.has_perm('centro_asistencia.delete_centro_asistencia')
	if agregar or actualizar or eliminar:
		return True
	else:
		raise PermissionDenied
		return False


# @permission_required(('centro_asistencia.add_centro_asistencia' or 'centro_asistencia.change_centro_asistencia' or 'centro_asistencia.delete_centro_asistencia'), raise_exception=True)
@login_required
@user_passes_test(permiso_requerido)
def lista_centro_asistencia(request):	
	groups_user = request.user.groups.values_list('name',flat=True)	
	for grupo in groups_user:				
		if grupo == 'SUPER ADMINISTRADOR':
			centros_asistencia = Centro_Asistencia.objects.order_by('pk')
			break
		elif grupo == 'JEFE DEPARTAMENTO':			
			# centros_asistencia = Centro_Asistencia.objects.filter(usuarios__dni=request.user)
			centros_asistencia = Centro_Asistencia.objects.administrado_por_mi(user=request.user)			
			break
		else:
			# USUARIO QUE PUEDE SER TÉCNICO U OTRO GRUPO AL QUE SEA ASIGNADO
			centros_asistencia = Centro_Asistencia.objects.asignado_para_mi(user=request.user)
	contexto ={'centros_asistencia': centros_asistencia}	
	return render(request, 'centro_asistencia/lista_centro_asistencia.html',contexto)



class Centro_Asistencia_DetailView(DetailView):		
	model = Centro_Asistencia
	def get_context_data(self, **kwargs):    
		context = super(Centro_Asistencia_DetailView, self).get_context_data(**kwargs)	
		context['jefes_departamento'] = Perfil.objects.filter(personal_operativo__centro_asistencia__id=self.object.id, personal_operativo__grupo__name='JEFE DEPARTAMENTO').distinct()
		###->context['jefes_departamento'] = Perfil.jefes_departamento.filter(centro_asistencia__id=self.object.id)
		###->context['asesores_tecnicos'] = Perfil.asesores_tecnicos.filter(centro_asistencia__id=self.object.id)
		context['asesores_tecnicos'] = Perfil.objects.filter(personal_operativo__centro_asistencia__id=self.object.id, personal_operativo__grupo__name='ASESOR TECNICO').distinct()
		return context
		# self.object -> ES EL OBJETO DEL QUE SE HABLA EN EL DETAILVIEW		
		# context['user_jefes_list'] = Perfil.jefes_departamento.all()		
		# context['user_asesores_list'] = Perfil.asesores_tecnicos.all()					
	@method_decorator(login_required)
	@method_decorator(permission_required('centro_asistencia.change_centro_asistencia', raise_exception=permission_required))
	# AGREGAR UN PERMISO -> ASIGNAR USUARIOS @method_decorator(permission_required('centro_asistencia.change_centro_asistencia'))
	def dispatch(self, *args, **kwargs):
		return super(Centro_Asistencia_DetailView, self).dispatch(*args, **kwargs)


class Centro_AsistenciaCreate(CreateView):
	model = Centro_Asistencia
	template_name = 'centro_asistencia/centro_asistencia_edit_form.html'
	form_class = form_agregar_centro_asistencia
		
	def form_valid(self, form):		
		centro_existente = Centro_Asistencia.objects.filter(nombre=form.cleaned_data['nombre'])
		if centro_existente:
			raise forms.ValidationError('Ya existe este centro')
					
		self.object = form.save()	 	
	 	centro_asistencia = self.object	 	
	 	usuario = self.request.user
	 	if usuario.has_perm('centro_asistencia.change_centro_asistencia'):	 		
	 		link = '<a href='+centro_asistencia.get_absolute_url()+'>%s</a>' % (centro_asistencia.nombre)
	 		editar = '<div class="col-sm-5"><a data-toggle="modal" href="/centro_asistencia/edit/%s" data-target="#modal_centro_asistencia" title="Editar Centro de Asistencia" data-tooltip class="btn btn-default"><span class="glyphicon glyphicon-pencil"></span></a></div>' % (centro_asistencia.id)
	 	else:
	 		link = '%s' % (centro_asistencia.nombre)
	 		editar = ''

	 	if usuario.has_perm('centro_asistencia.delete_centro_asistencia'):	 				 		
	 		eliminar = '<div class="col-sm-5"><a data-toggle="modal" href="/centro_asistencia/%s/delete" data-target="#delele_modal_ca" title="Eliminar" data-tooltip class="btn btn-danger"><span class="glyphicon glyphicon-trash"></span></a></div>' % (centro_asistencia.id)
	 	else:		 		
	 		eliminar = ''

	 	if self.request.is_ajax():	 		
	 		fila = '<tr id="tr_centro_asistencia%s"><td>%s</td><td> %s</td><td><div class="row-fluid">%s %s</div></td></tr>' % (centro_asistencia.id, link, centro_asistencia.descripcion, editar, eliminar)
	 		ctx = {'respuesta':'create', 'fila':fila, 'id':centro_asistencia.id,}
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	else:
	 		return super(Centro_AsistenciaCreate, self).form_valid(form)



class Centro_AsistenciaUpdate(UpdateView):
	model = Centro_Asistencia
	template_name = 'centro_asistencia/centro_asistencia_edit_form.html'
	form_class = Centro_Asistencia_UpdateForm	

	@method_decorator(login_required)
	@method_decorator(permission_required('centro_asistencia.change_centro_asistencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):		
		self.centro_asistencia_id = kwargs['pk']
		return super(Centro_AsistenciaUpdate, self).dispatch(*args, **kwargs)
		
	def form_valid(self, form):
		try:
			form.registro_nombre_duplicado(id_centro= self.object.id)		
		except ValidationError:			
			form._errors["nombre"] = ErrorList([u"Ya existe un centro de asistencia con ese nombre."])						
			return super(Centro_AsistenciaUpdate, self).form_invalid(form)
		if self.request.is_ajax():
			form.save()
			centro_asistencia = self.object	 	
	 		usuario = self.request.user
		 	
		 	if usuario.has_perm('centro_asistencia.change_centro_asistencia'):	 		
		 		link = '<a href='+centro_asistencia.get_absolute_url()+'>%s</a>' % (centro_asistencia.nombre)
		 		editar = '<div class="col-sm-5"><a data-toggle="modal" href="/centro_asistencia/edit/%s" data-target="#modal_centro_asistencia" title="Editar Centro de Asistencia" data-tooltip class="btn btn-default"><span class="glyphicon glyphicon-pencil"></span></a></div>' % (centro_asistencia.id)
		 	else:
		 		link = '%s' % (centro_asistencia.nombre)
		 		editar = ''

		 	if usuario.has_perm('centro_asistencia.delete_centro_asistencia'):	 				 		
		 		eliminar = '<div class="col-sm-5"><a data-toggle="modal" href="/centro_asistencia/%s/delete" data-target="#delele_modal_ca" title="Eliminar" data-tooltip class="btn btn-danger"><span class="glyphicon glyphicon-trash"></span></a></div>' % (centro_asistencia.id)
		 	else:		 		
		 		eliminar = ''

	 		fila = '<tr id="tr_centro_asistencia%s"><td>%s</td><td> %s</td><td><div class="row-fluid">%s %s </div></td></tr>' % (centro_asistencia.id, link, centro_asistencia.descripcion, editar, eliminar)	 				
			ctx = {'respuesta':'update', 'fila':fila, 'id':centro_asistencia.id,}
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	else:
	 		return super(Centro_AsistenciaUpdate, self).form_valid(form)

class Centro_AsistenciaDelete(DeleteView):
	model = Centro_Asistencia
	
	@method_decorator(login_required)
	@method_decorator(permission_required('centro_asistencia.delete_centro_asistencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(Centro_AsistenciaDelete, self).dispatch(*args, **kwargs)	

	def delete(self, request, *args, **kwargs):	
		self.object = self.get_object()
		id_centro_asistencia = self.object.id
		try:
			self.object.delete()
		except IntegrityError:
			self.object.estado = False
			self.object.save()		
		ctx = {'respuesta': 'ok', 'id':id_centro_asistencia,}
		return HttpResponse(json.dumps(ctx), content_type='application/json')
 	

class Centro_Asistencia_General(ListView):
	model = Centro_Asistencia
	template_name = 'centro_asistencia/centros_asistencia_generalist.html'
	context_object_name = 'centros_asistencia'

	def get_queryset(self):		
		queryset = Centro_Asistencia.objects.filter(estado=True)		
		return queryset

	@method_decorator(login_required)	
	def dispatch(self, *args, **kwargs):
		return super(Centro_Asistencia_General, self).dispatch(*args, **kwargs)



		
##################
# MODEL SERVICIO #
##################

class ServicioCreate(CreateView):
	model = Servicio
	template_name = 'centro_asistencia/servicio_edit_form.html'
	form_class = ServicioForm

	def get_context_data(self, **kwargs):
		ctx = super(ServicioCreate, self).get_context_data(**kwargs)
		ctx['centro'] = self.kwargs['centro']
		return ctx

	@method_decorator(login_required)
	@method_decorator(permission_required('centro_asistencia.add_servicio', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.servicio_centro = Centro_Asistencia.objects.get(pk=self.kwargs['centro'])
		return super(ServicioCreate, self).dispatch(*args, **kwargs)		

	def form_valid(self, form):
		self.object = form.save(commit=False)
		centro = Centro_Asistencia.objects.get(pk=self.kwargs['centro'])
		self.object.centro = centro		
	 	self.object.save()
	 	servicio = self.object
	 	if self.request.is_ajax():	 		
	 		fila = '<tr id="tr_servicio%s"><td><a data-toggle="modal" href="/servicio/%s" data-target="#modal" title="Editar Servicio" data-tooltip>%s</a></td><td> %s</td> <td> %s</td> <td> %s</td> '\
	 				'<td><a href="/servicio/%s/delete" role="button" class="btn btn-danger delete" data-toggle="modal" data-target="#delele_modal" title="Eliminar Servicio" data-nombre="%s" data-id="%s">'\
	 				'<span class="glyphicon glyphicon-trash"></span></a></td></tr>' % (servicio.id, servicio.id, servicio.nombre, timedeltaformat(servicio.t_minimo), timedeltaformat(servicio.t_normal), timedeltaformat(servicio.t_maximo), servicio.id, servicio.nombre,servicio.id)	 		
	 		ctx = {'respuesta':'create', 'fila':fila, 'id':servicio.id,}	
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	else:
	 		return super(ServicioCreate, self).form_valid(form)

class ServicioUpdate(UpdateView):
	model = Servicio
	template_name = 'centro_asistencia/servicio_edit_form.html'
	form_class = ServicioForm 	

	@method_decorator(login_required)
	@method_decorator(permission_required('centro_asistencia.change_servicio', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):		
		self.servicio_id = kwargs['pk']		
		return super(ServicioUpdate, self).dispatch(*args, **kwargs)
	def form_valid(self, form):		
	 	form.save()
	 	if self.request.is_ajax():	 		
	 		servicio = self.object
	 		fila = '<tr id="tr_servicio%s"><td><a data-toggle="modal" href="/servicio/%s" data-target="#modal" title="Editar Servicio" data-tooltip>%s</a></td><td> %s</td> <td> %s</td> <td> %s</td> '\
	 				'<td><a href="/servicio/%s/delete" role="button" class="btn btn-danger delete" data-toggle="modal" data-target="#delele_modal" title="Eliminar Servicio" data-nombre="%s" data-id="%s">'\
	 				'<span class="glyphicon glyphicon-trash"></span></a></td></tr>' % (servicio.id, servicio.id, servicio.nombre, timedeltaformat(servicio.t_minimo), timedeltaformat(servicio.t_normal), timedeltaformat(servicio.t_maximo), servicio.id, servicio.nombre,servicio.id)
	 		id_servicio = servicio.id
	 		ctx = {'respuesta':'update', 'fila':fila, 'id':id_servicio,}	
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	else:
	 		return super(ServicioUpdate, self).form_valid(form)

class ServicioDelete(DeleteView):
	model = Servicio

	@method_decorator(login_required)
	@method_decorator(permission_required('centro_asistencia.delete_servicio', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ServicioDelete, self).dispatch(*args, **kwargs)	


	def delete(self, request, *args, **kwargs):	
		self.object = self.get_object()
		id_servicio = self.object.id
		self.object.estado = False
		self.object.save()
		ctx = {'respuesta': 'ok', 'id':id_servicio,}
		return HttpResponse(json.dumps(ctx), content_type='application/json')



	# def get_success_url(self):		
	# 	return '/centro_asistencia/%i' %(self.object.centro.id)
	
	# 	servicio = Servicio.objects.get(id=self.servicio_id)
	# 	centro_asistencia = Centro_Asistencia.objects.get(pk=servicio_centro_id)
	# 	return HttpResponse(render_to_string('centro_asistencia/servicio_edit_form_success.html', {'servicio': servicio}))	
	
	### PUEDE LLEGAR A SERVIR ###
	# fields = ['nombre', 'descripcion',]
	# form_class = forms.models.modelform_factory(Servicio, 
	# 	fields={'nombre', 'descripcion', },
	# 	widgets={
	# 		'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del servicio.',}),
	# 		'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripción del servicio.',})
	# 	}, 
	# 	labels ={
	# 		'nombre' : 'Nombre:',
	# 		'descripcion' : 'Descripción:',
	# 	},)
	# def get_form_class(self):		
	# 	print self.form_class._meta.fields
	# 	return self.form_class

# def areas_de_produccion_view(request):
# 	if request.user.is_authenticated():	
# 		areas= AreaProduccion.objects.order_by('pk')
# 		ctx= {'areas':areas}
# 		return render(request,'producto/productionArea/productionAreas.html',ctx)
# 	else:
# 		return HttpResponseRedirect(LOGIN_REDIRECT_URL)

# DetailView
# http://www.dailymotion.com/video/x2b0m1w_15-detailview-curso-pro-de-django-1-6_school

#AJAX CON DJANGO
#https://claudiomelendrez.wordpress.com/2013/04/03/ajax-django-part-1/

##############
# SERVICIO ---- CREATEVIEWS, UPDATEVIEWS, DELETEVIEWS
# http://dmorgan.info/posts/django-views-bootstrap-modals/
# AUTOCOMPLETE
# http://laempresaconsoftwareabierto.blogspot.com/2013/09/jquery-autocomplete-en-django.html

##############

# === OPCIONES PARA VER ERRORES DE FORMULARIO 
# form._errors.get('nombre', ErrorList())
# self._errors['field1'] = self._errors.get('field1', ErrorList())



# from functools import partial
# permission_required = partial(permission_required, raise_exception=True)

# https://github.com/luchitoflores/ekklesia/blob/master/ciudades/views.py
# CRUD DJANGO CON VIEWS... 
# https://rayed.com/wordpress/?p=1266
# Create your views here.

#DECORADORES 
#https://github.com/django/django/blob/master/django/contrib/auth/decorators.py