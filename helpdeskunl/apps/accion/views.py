# -*- coding: utf-8 -*-
#REQUEST
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import json
#MODELS
from helpdeskunl.apps.accion.form import *
from helpdeskunl.apps.accion.models import *
from helpdeskunl.apps.home.models import *
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.problema.models import *
from helpdeskunl.apps.cambio.models import *

from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import ModelFormMixin
from django.contrib.messages.views import SuccessMessageMixin

# METODOS DECORADORES
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

#EXCEPCIONES
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

#MENSAJES
from django.contrib import messages

#FECHAS
from datetime import datetime

#CONSULTAS
from django.db.models import Q


##############################
#         PERMISOS           #
##############################
def es_tecnico(user):
	asesores = Perfil.asesores_tecnicos.all()	
	if user in asesores:
		return True
	else:
		raise PermissionDenied
		return False

def es_jefe(user):
	jefes_departamento = Perfil.jefes_departamento.all()	
	if user in jefes_departamento:
		return True
	else:
		raise PermissionDenied
		return False

def soy_propietario_incidencia(self):	
	incidencia = get_object_or_404(Incidencia, pk=self.incidencia_id)
	usuario = self.request.user
	if incidencia.solicitante == usuario:
		return True
	else:
		return False

def permiso_incidencia_detail(self):
	incidencia = get_object_or_404(Incidencia, pk=self.kwargs['incidencia_id'])
	
	asesores = Perfil.asesores_tecnicos.filter(personal_operativo__centro_asistencia=incidencia.centro_asistencia).distinct()
	jefes_departamento = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia=incidencia.centro_asistencia).distinct()
	respuesta = False

	if self.request.user in asesores:
		respuesta = True		
	if self.request.user in jefes_departamento:
		respuesta = True	

	return respuesta

##############################
#    DIAGNOSTICO INICIAL     #
##############################

class Diagnostico_Inicial_Create(SuccessMessageMixin, CreateView):
	model = Diagnostico_Inicial	
	template_name = 'accion/diagnostico/diagnostico_inicial.html'
	form_class = Diagnostico_InicialForm	
	success_message = u"Diagnostico creado con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.add_diagnostico_inicial', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))		
		if incidencia.es_vigente(request=self.request):				
			return super(Diagnostico_Inicial_Create, self).dispatch(*args, **kwargs)
		else:
			messages.add_message(self.request, messages.ERROR, 'No se puede diagnosticar. La incidencia ha expirado')			
			return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':incidencia.id}))		

	def get_context_data(self, **kwargs):
		context = super(Diagnostico_Inicial_Create, self).get_context_data(**kwargs)				
		incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))		
		context['bienes_incidencia'] = incidencia.bienes.all()			
		context['incidencia'] = incidencia
		return context

	def form_valid(self, form):
		self.object = form.save()		
		querty =  self.request.POST.copy()
		try:
			for idbien in querty.pop('bien'):
				bien = Bien.objects.get(pk=int(idbien))
				diagnostico_bien = Diagnostico_Bien(bien=bien, diagnostico= self.object, recibido=True)
				diagnostico_bien.save()
		except Exception, e:
			print e		
		
		self.object.tecnico = self.request.user
		self.object.incidencia = self.get_context_data()['incidencia']
		self.object.save()		

		return super(Diagnostico_Inicial_Create, self).form_valid(form)

	def get_success_url(self):
		try:
			return reverse('accion_list', kwargs={'incidencia_id': self.kwargs['incidencia_id']})
		except Exception, e:
			print e


class Diagnostico_Inicial_Update(SuccessMessageMixin, UpdateView):
	model = Diagnostico_Inicial	
	template_name = 'accion/diagnostico/diagnostico_inicial.html'
	form_class = Diagnostico_InicialForm	
	success_message = u"Diagnostico actualizado con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.change_diagnostico_inicial', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.diagnostico_id = kwargs['pk']	
		diagnostico = get_object_or_404(Diagnostico_Inicial, pk=int(self.diagnostico_id))		
		
		if diagnostico.incidencia.es_vigente(request=self.request):				
			return super(Diagnostico_Inicial_Update, self).dispatch(*args, **kwargs)
		else:
			messages.add_message(self.request, messages.ERROR, 'No se puede actualizar. La incidencia ha expirado')			
			return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':diagnostico.incidencia.id}))		
	
		

	def get_context_data(self, **kwargs):		
		context = super(Diagnostico_Inicial_Update, self).get_context_data(**kwargs)		
		diagnostico = self.object
		incidencia = get_object_or_404(Incidencia, pk=int(diagnostico.incidencia.id))
		bienes_recibidos = 	Bien.objects.filter(diagnostico_inicial__incidencia=incidencia).distinct()
		bienes_no_recibidos = list()

		for bien in incidencia.bienes.all():
			if bien not in bienes_recibidos:
				bienes_no_recibidos.append(bien)

		context['bienes_incidencia'] = bienes_no_recibidos
		context['bienes_recibidos'] = bienes_recibidos
		context['incidencia'] = incidencia		

		return context

	def form_valid(self, form):
		self.object = form.save()		
		bienes_recibidos = 	Diagnostico_Bien.objects.filter(diagnostico__id=self.object.id).distinct()
		bienes_recibidos.delete()

		querty =  self.request.POST.copy()
		try:
			for idbien in querty.pop('bien'):
				bien = Bien.objects.get(pk=int(idbien))
				diagnostico_bien = Diagnostico_Bien(bien=bien, diagnostico= self.object, recibido=True)
				diagnostico_bien.save()
		except Exception, e:
			print e		
		
		self.object.tecnico = self.request.user
		self.object.incidencia = self.get_context_data()['incidencia']
		self.object.save()		

		return super(Diagnostico_Inicial_Update, self).form_valid(form)

	def get_success_url(self):
		try:
			return reverse('accion_list', kwargs={'incidencia_id': self.object.incidencia.id})
		except Exception, e:
			print e

##############################
#         ACCIONES           #
##############################
class AccionList(ListView):
	model = Accion
	template_name = 'accion/accion/accion_list.html'
	context_object_name = 'acciones'

	@method_decorator(login_required)	
	def dispatch(self, *args, **kwargs):
		if permiso_incidencia_detail(self):
			return super(AccionList, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied

	def get_context_data(self, **kwargs):
		context = super(AccionList, self).get_context_data(**kwargs)		
		incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))
		try:
			diagnostico = Diagnostico_Inicial.objects.get(incidencia = incidencia)
		except Diagnostico_Inicial.DoesNotExist:
			diagnostico = None
		
		context['incidencia'] = incidencia
		context['diagnostico'] = diagnostico
		return context

	def get_queryset(self):
		incidencia = self.kwargs['incidencia_id']	
		queryset = Accion.objects.filter(Q(estado=True), (Q(incidencia__id=incidencia)|Q(problema__incidencia__id=incidencia)|Q(cambio__problema__incidencia__id=incidencia)))		
		return queryset


class AccionCreate(SuccessMessageMixin, CreateView):
	model = Accion
	template_name = 'accion/accion/accion_create_form.html'
	form_class = AccionForm	
	success_message = u"%(titulo)s se ha creado con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.add_accion', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		if permiso_incidencia_detail(self):
			incidencia = get_object_or_404(Incidencia, pk= int(self.kwargs['incidencia_id']))
			if incidencia.es_vigente(request=self.request):				
				return super(AccionCreate, self).dispatch(*args, **kwargs)
			else:
				messages.add_message(self.request, messages.ERROR, 'Imposible crear acción. La incidencia ha expirado')			
				return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':incidencia.id}))
		else:
			raise PermissionDenied
	
	def form_valid(self, form):
		incidencia = get_object_or_404(Incidencia, pk= int(self.kwargs['incidencia_id']))
		self.object = form.save(commit=False)		
		self.object.incidencia = incidencia
		self.object.nivel = incidencia.nivel
		self.object.tecnico = self.request.user
		self.object.save()
		querty =  self.request.POST.copy()
		try:
			for recurso in querty.pop('recursos'):
				self.recursos = recurso
		except Exception, e:
			print e
		return super(AccionCreate, self).form_valid(form)

	def get_success_url(self):
		if self.recursos == 'NO':
			try:
				return reverse('solicitudes_list', kwargs={'incidencia_id': self.object.incidencia.id, 'accion_id': self.object.id})
			except Exception, e:
				print e
		else:
			try:
				return reverse('accion_list', kwargs={'incidencia_id': self.object.incidencia.id})
			except Exception, e:
				print e

	def get_context_data(self, **kwargs):
		context = super(AccionCreate, self).get_context_data(**kwargs)				
		incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))		
		context['incidencia'] = incidencia
		return context

class AccionUpdate(SuccessMessageMixin, UpdateView):
	model = Accion	
	template_name = 'accion/accion/accion_create_form.html'
	form_class = AccionForm	
	success_message = u"%(titulo)s se ha actualizado con éxito."

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.change_accion', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.accion_id = kwargs['pk']		 
		try:
			accion = Accion.objects.get(pk = int(self.accion_id))
		except Accion.DoesNotExist:
			accion = None
		
		self.kwargs['incidencia_id'] = accion.incidencia.id			

		if permiso_incidencia_detail(self):
			if accion.incidencia.es_vigente(request=self.request):				
				return super(AccionCreate, self).dispatch(*args, **kwargs)
			else:
				messages.add_message(self.request, messages.ERROR, 'Imposible actualizar. La incidencia ha expirado')			
				return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':accion.incidencia.id}))
			return super(AccionUpdate, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied
	
	def get_context_data(self, **kwargs):		
		context = super(AccionUpdate, self).get_context_data(**kwargs)				
		incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))		
		context['incidencia'] = incidencia
		return context

	def form_valid(self, form):
		incidencia = get_object_or_404(Incidencia, pk= int(self.kwargs['incidencia_id']))
		self.object = form.save(commit=False)		
		self.object.tecnico = self.request.user
		self.object.save()
		querty =  self.request.POST.copy()
		try:
			for recurso in querty.pop('recursos'):
				self.recursos = recurso
		except Exception, e:
			print e
		return super(AccionUpdate, self).form_valid(form)

	def get_success_url(self):
		if self.recursos == 'SI':
			try:
				return reverse('solicitudes_list', kwargs={'incidencia_id': self.object.incidencia.id, 'accion_id': self.object.id})
			except Exception, e:
				print e
		else:
			try:
				return reverse('accion_list', kwargs={'incidencia_id': self.object.incidencia.id})
			except Exception, e:
				print e


class AccionDelete(DeleteView):
	model = Accion
	template_name = 'accion/accion/accion_confirm_delete.html'	
	success_message = 'Acción eliminada con éxito'	

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.delete_accion', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.accion_id = kwargs['pk']	
		return super(AccionDelete, self).dispatch(*args, **kwargs)			

	def delete(self, request, *args, **kwargs):	
		self.object = self.get_object()
		id_accion = self.object.id		
		accion = get_object_or_404(Accion, pk=id_accion)				

		if accion.incidencia.es_vigente(request=request):				
			if accion.solicitud_recurso_set.all():
				messages.add_message(self.request, messages.ERROR, 'No se puede eliminar. Se han solicitado recursos en esta acción')			
			else:
				self.object.estado = False				
				self.object.save()		
				messages.success(self.request, self.success_message)
		else:
			messages.add_message(self.request, messages.ERROR, 'No se puede eliminar. La incidencia ha expirado')
		return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':accion.incidencia.id}))


		


##############################
#    SOLICITUDES DE RECURSO  #
##############################

class SolicitudesList(ListView):
	model = Solicitud_Recurso
	template_name = 'accion/recurso/recurso_list.html'
	context_object_name = 'recursos'

	@method_decorator(login_required)	
	def dispatch(self, *args, **kwargs):
		if permiso_incidencia_detail(self):
			return super(SolicitudesList, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied

	def get_context_data(self, **kwargs):
		context = super(SolicitudesList, self).get_context_data(**kwargs)		
		#incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))
		accion = get_object_or_404(Accion, pk=int(self.kwargs['accion_id']))		
		#context['incidencia'] = incidencia
		context['accion'] = accion		
		return context

	def get_queryset(self):
		accion = self.kwargs['accion_id']	
		queryset = Solicitud_Recurso.objects.filter(Q(estado=True), Q(accion_id=accion))		
		return queryset



class SolicitudCreate(SuccessMessageMixin, CreateView):
	model = Solicitud_Recurso
	template_name = 'accion/recurso/recurso_create_form.html'
	form_class = Solicitud_RecursoForm	
	success_message = u"Solicitud de recurso se ha creado con éxito."

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.add_solicitud_recurso', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		accion = get_object_or_404(Accion, pk= int(self.kwargs['accion_id']))
		self.kwargs['incidencia_id'] = accion.incidencia.id

		if permiso_incidencia_detail(self):
			return super(SolicitudCreate, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied
	
	def form_valid(self, form):
		accion = get_object_or_404(Accion, pk= int(self.kwargs['accion_id']))		
		self.object = form.save(commit=False)		
		self.object.accion = accion		
		self.object.tecnico = self.request.user
		self.object.save()
		return super(SolicitudCreate, self).form_valid(form)

	def get_success_url(self):
		try:
			return reverse('solicitudes_list', kwargs={'accion_id': self.object.accion.id, 'incidencia_id': self.object.accion.incidencia.id})
		except Exception, e:
			print e

	def get_context_data(self, **kwargs):
		context = super(SolicitudCreate, self).get_context_data(**kwargs)				
		accion = get_object_or_404(Accion, pk=int(self.kwargs['accion_id']))				
		context['accion'] = accion
		return context

class SolicitudUpdate(SuccessMessageMixin, UpdateView):
	model = Accion	
	template_name = 'accion/accion/accion_create_form.html'
	form_class = AccionForm	
	success_message = u"%(titulo)s se ha actualizado con éxito."

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.change_accion', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.accion_id = kwargs['pk']		 
		try:
			accion = Accion.objects.get(pk = int(self.accion_id))
		except Accion.DoesNotExist:
			accion = None
		
		self.kwargs['incidencia_id'] = accion.incidencia.id			

		if permiso_incidencia_detail(self):			
			return super(SolicitudUpdate, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied
	
	def get_context_data(self, **kwargs):		
		context = super(SolicitudUpdate, self).get_context_data(**kwargs)				
		incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))		
		context['incidencia'] = incidencia
		return context

	def form_valid(self, form):
		incidencia = get_object_or_404(Incidencia, pk= int(self.kwargs['incidencia_id']))
		self.object = form.save(commit=False)		
		self.object.tecnico = self.request.user
		self.object.save()
		querty =  self.request.POST.copy()
		try:
			for recurso in querty.pop('recursos'):
				self.recursos = recurso
		except Exception, e:
			print e
		return super(SolicitudUpdate, self).form_valid(form)

	def get_success_url(self):
		if self.recursos == 'SI':
			try:
				return reverse('solicitudes_list', kwargs={'incidencia_id': self.object.incidencia.id, 'accion_id': self.object.id})
			except Exception, e:
				print e
		else:
			try:
				return reverse('accion_list', kwargs={'incidencia_id': self.object.incidencia.id})
			except Exception, e:
				print e


#AGREGAR CUANDO CREE LA SOLICITUD DE INCIDENCIA
# # AGREGA LA INCIDENCIA AL HISTORIAL CON FECHAS
		# historial = Historial_Incidencia(incidencia= self.object, tipo='0', fecha = datetime.now() , tiempo_restante= None)
		# historial.save()