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
from helpdeskunl.apps.accion.reports import convertHtmlToPdf
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.problema.models import *
from helpdeskunl.apps.cambio.models import *
from django.conf import settings

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
from django.utils import timezone
from django.utils import formats

#CONSULTAS
from django.db.models import Q

# ENVIO DE CORREO ELECTRONICO
from django.core.mail import send_mail, EmailMessage


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
			if incidencia.estado_incidencia == ESTADO_ABIERTA:
				return super(Diagnostico_Inicial_Create, self).dispatch(*args, **kwargs)
			else:			
				messages.add_message(self.request, messages.ERROR, 'No se puede diagnosticar')			
				return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':incidencia.id}))		
		else:			
			messages.add_message(self.request, messages.ERROR, 'No se puede diagnosticar. La incidencia está cerrada')			
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
			if diagnostico.incidencia.estado_incidencia == ESTADO_ABIERTA:
				return super(Diagnostico_Inicial_Update, self).dispatch(*args, **kwargs)
			else:			
				messages.add_message(self.request, messages.ERROR, 'No se puede diagnosticar')			
		else:
			messages.add_message(self.request, messages.ERROR, 'No se puede actualizar. La incidencia está cerrada')			
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
				if incidencia.estado_incidencia == ESTADO_ABIERTA:				
					return super(AccionCreate, self).dispatch(*args, **kwargs)
				else:			
					messages.add_message(self.request, messages.ERROR, 'No se puede crear acciones')				
			else:
				messages.add_message(self.request, messages.ERROR, 'Imposible crear acción. La incidencia está cerrada')			
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
	success_message = u"%(titulo)s se ha actualizado con éxito"

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
				if accion.tecnico == self.request.user:								
					if accion.incidencia.estado_incidencia == ESTADO_ABIERTA:				
						return super(AccionUpdate, self).dispatch(*args, **kwargs)
					else:			
						messages.add_message(self.request, messages.ERROR, 'No se puede actualizar acciones')
				else:
					raise PermissionDenied
			else:
				messages.add_message(self.request, messages.ERROR, 'Imposible actualizar. La incidencia está cerrada')			
			return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':accion.incidencia.id}))			
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

		if self.object.tecnico != self.request.user:			
			messages.add_message(self.request, messages.ERROR, 'Permiso Denegado')
			return HttpResponseRedirect(reverse_lazy('accion_list', kwargs={'incidencia_id':accion.incidencia.id}))

		if accion.incidencia.es_vigente(request=request):				
			if accion.solicitud_recurso_set.all():
				messages.add_message(self.request, messages.ERROR, 'No se puede eliminar. Se han solicitado recursos en esta acción')			
			else:
				self.object.estado = False				
				self.object.save()		
				messages.success(self.request, self.success_message)
		else:
			messages.add_message(self.request, messages.ERROR, 'No se puede eliminar. La incidencia está cerrada')
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


class AccionSolicitudesList(ListView):
	model = Solicitud_Recurso
	template_name = 'accion/accion/accion_list_onsolicitudes.html'
	context_object_name = 'recursos'

	@method_decorator(login_required)	
	def dispatch(self, *args, **kwargs):
		if permiso_incidencia_detail(self):
			return super(AccionSolicitudesList, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied

	def get_context_data(self, **kwargs):
		context = super(AccionSolicitudesList, self).get_context_data(**kwargs)		
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
		queryset = Solicitud_Recurso.objects.filter(Q(estado=True), Q(accion__incidencia_id=incidencia))		
		return queryset



class SolicitudCreate(SuccessMessageMixin, CreateView):
	model = Solicitud_Recurso
	template_name = 'accion/recurso/recurso_create_form.html'
	form_class = Solicitud_RecursoForm	
	success_message = u"Solicitud de recurso se ha creado con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.add_solicitud_recurso', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		accion = get_object_or_404(Accion, pk= int(self.kwargs['accion_id']))
		self.kwargs['incidencia_id'] = accion.incidencia.id		
		if permiso_incidencia_detail(self):
			if accion.incidencia.es_vigente(request=self.request):	
				if accion.tecnico == self.request.user:								
					return super(SolicitudCreate, self).dispatch(*args, **kwargs)
				else:
					raise PermissionDenied
			else:
				messages.add_message(self.request, messages.ERROR, 'No se puede agregar. La incidencia está cerrada')			
				return HttpResponseRedirect(reverse_lazy('solicitudes_list', kwargs={'incidencia_id':accion.incidencia.id, 'accion_id':accion.id}))
		else:
			raise PermissionDenied
	
	def form_valid(self, form):
		accion = get_object_or_404(Accion, pk= int(self.kwargs['accion_id']))		
		self.object = form.save(commit=False)		
		self.object.accion = accion		
		self.object.tecnico = self.request.user
		self.object.save()

		# SI EL RECURSO SOLICITADO ES HACIA EL USUARIO QUE GENERA LA INCIDENCIA			
		if self.object.proveedor.perfil:			
			if self.object.proveedor.perfil == accion.incidencia.solicitante:				
				
				# CORREGIR AGREGAR URL PARA LISTAS DE SOLICITUDES DE RECURSO EN USUARIO FINAL
				url = base64.encodestring(reverse_lazy('incidencia_centro_list'))
				# 

				notificacion = Notificacion(remitente=self.request.user, destinatario = self.object.proveedor.perfil , tipo = '5')
				notificacion.save()			
				notificacion.construir_notificacion(extra=self.object.accion.incidencia.titulo)
				
				if self.object.proveedor == self.request.user:
					messages.add_message(self.request, messages.INFO, notificacion.mensaje)
				else:
					notificacion.notificar()

		# ENVIAR CORREO ELECTRÓNICO INFORMANDO LA SOLICITUD
		if self.object.notificar_email:
			centro_asistencia = self.object.accion.incidencia.centro_asistencia
			mensaje = "Se ha solicitado un recurso desde el %s, que se detalla en el siguiente archivo adjunto." %(centro_asistencia.nombre) 
			if self.proveedor.perfil:
				correo_para = self.proveedor.perfil.email
			else:
				correo_para = self.object.proveedor.correo
			email = EmailMessage('SOLICITUD DE RECURSO', mensaje , settings.EMAIL_HOST_USER ,[correo_para]) 		
			email.attach_file(convertHtmlToPdf(self.object.id))
			email.send(fail_silently=False)

		else:
			# NO SEN ENVIA EL EMAIL PERO SE CREA EL REPORTE
			convertHtmlToPdf(self.object.id)
		
		# DEJAR O NO EN ESPERA 
		if self.object.esperar: # 0 == SI			
			solicitudes = Solicitud_Recurso.objects.filter(Q(estado=True), Q(esperar=True), ~Q(id=self.object.id))
			
			# SI HO HAY SOLICITUDES QUE DEJEN EN ESPERA A LA INCIDENCIA 			
			if not solicitudes or (accion.incidencia.estado_incidencia != ESTADO_PENDIENTE):				
				# función de esperar				
				incidencia = accion.incidencia			
				incidencia.caduca = None				
				incidencia.estado_incidencia = ESTADO_PENDIENTE				
				incidencia.save()				
				#calcular duracion restante
				historial_aux = Historial_Incidencia.objects.filter(incidencia=incidencia).latest('id')								
				hoy = timezone.now()				
				utilizado = hoy - historial_aux.fecha				
				restante= historial_aux.tiempo_restante - utilizado				

				historial = Historial_Incidencia(incidencia= accion.incidencia, tipo='3', fecha = datetime.now() , tiempo_restante= restante)				
				historial.save()				

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

	def get_form_kwargs(self):
		accion = get_object_or_404(Accion, pk=int(self.kwargs['accion_id']))				
		kwargs = super(SolicitudCreate, self).get_form_kwargs()
		kwargs.update({'my_user': accion.incidencia.solicitante})		
		return kwargs

class SolicitudUpdate(SuccessMessageMixin, UpdateView):
	model = Solicitud_Recurso	
	template_name = 'accion/recurso/recurso_create_form.html'
	form_class = Solicitud_RecursoForm	
	success_message = u"Solicitud de recurso se ha acutalizado con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.change_solicitud_recurso', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):

		self.solicitud_id = kwargs['pk']		 
		try:
			solicitud = Solicitud_Recurso.objects.get(pk = int(self.solicitud_id))
		except Solicitud_Recurso.DoesNotExist:
			Solicitud = None
		
		self.kwargs['incidencia_id'] = solicitud.accion.incidencia.id		
		
		if solicitud.despachado:
			messages.add_message(self.request, messages.ERROR, 'No se puede actualizar. Este recurso ya se ha despachado')			
			return HttpResponseRedirect(reverse_lazy('solicitudes_list', kwargs={'incidencia_id':solicitud.accion.incidencia.id, 'accion_id':solicitud.accion.id}))

		if permiso_incidencia_detail(self):
			if solicitud.accion.incidencia.es_vigente(request=self.request):
				if solicitud.accion.tecnico == self.request.user:								
					return super(SolicitudUpdate, self).dispatch(*args, **kwargs)
				else:
					raise PermissionDenied
			else:
				messages.add_message(self.request, messages.ERROR, 'No se puede actualizar. La incidencia está cerrada')			
				return HttpResponseRedirect(reverse_lazy('solicitudes_list', kwargs={'incidencia_id':solicitud.accion.incidencia.id, 'accion_id':solicitud.accion.id}))							
		else:
			raise PermissionDenied
	
	def get_context_data(self, **kwargs):		
		context = super(SolicitudUpdate, self).get_context_data(**kwargs)				
		context['accion'] = self.object.accion
		return context

	def get_form_kwargs(self):
		kwargs = super(SolicitudUpdate, self).get_form_kwargs()
		kwargs.update({'my_user': self.object.accion.incidencia.solicitante})		
		return kwargs

	def form_valid(self, form):
		
		solicitud_aux = Solicitud_Recurso.objects.get(pk=int(self.object.id))

		anterior_esperar = solicitud_aux.esperar
		anterior_notificar_email = solicitud_aux.notificar_email
		anterior_contacto = solicitud_aux.proveedor


		self.object = form.save(commit=False)
		self.object.tecnico = self.request.user
		self.object.save()

		# SI EL RECURSO SOLICITADO ES HACIA EL USUARIO QUE GENERA LA INCIDENCIA	
		if anterior_contacto != self.object.proveedor:
			if anterior_notificar_email:
				self.object.proveedor = anterior_contacto
				self.object.save()
				messages.add_message(self.request, messages.ERROR,'No es posible cambiar de proveedor porque ya se ha notificado antes')
			else:
				if anterior_contacto.perfil:
					# ELIMINAR SOLICITUD DE RECURSO
					url = base64.encodestring(reverse_lazy('solicitudes_list', kwargs={'accion_id': self.object.accion.id ,'incidencia_id': self.object.accion.incidencia.id}))

					notificacion = Notificacion(remitente=self.request.user, destinatario = anterior_contacto.perfil , tipo = '7', dirigir=url)
					notificacion.save()			
					notificacion.construir_notificacion(extra=self.object.accion.incidencia.titulo)
					# SI EL PROVEEDOR SOY YO
					if self.object.proveedor == self.request.user:
						messages.add_message(self.request, messages.INFO, notificacion.mensaje)
					else:
						notificacion.notificar()
				
				if self.object.proveedor.perfil:					
					# CORREGIR EL MISMO DE MAS ARRIBA TIPO 5
					url = base64.encodestring(reverse_lazy('solicitudes_list', kwargs={'accion_id': self.object.accion.id ,'incidencia_id': self.object.accion.incidencia.id}))
					#
					notificacion = Notificacion(remitente=self.request.user, destinatario = self.object.proveedor.perfil , tipo = '5', dirigir=url)
					notificacion.save()			
					notificacion.construir_notificacion(extra=self.object.accion.incidencia.titulo)
					
					if self.object.proveedor == self.request.user:
						messages.add_message(self.request, messages.INFO, notificacion.mensaje)
					else:
						notificacion.notificar()
		else:
			if self.object.proveedor.perfil:			
				if self.object.proveedor.perfil == self.object.accion.incidencia.solicitante:	
					# CORREGIR LO MISMO DEL TIPO 5
					url = base64.encodestring(reverse_lazy('solicitudes_list', kwargs={'accion_id': self.object.accion.id ,'incidencia_id': self.object.accion.incidencia.id}))			
					
					notificacion = Notificacion(remitente=self.request.user, destinatario = self.object.proveedor.perfil , tipo = '6', dirigir=url)
					notificacion.save()			
					notificacion.construir_notificacion(extra=self.object.accion.incidencia.titulo)
					# SI EL PROVEEDOR SOY YO
					if self.object.proveedor == self.request.user:
						messages.add_message(self.request, messages.INFO, notificacion.mensaje)
					else:
						notificacion.notificar()

		if self.object.notificar_email: #si actualmente
			if anterior_notificar_email: 
				convertHtmlToPdf(self.object.id)
			else:
				centro_asistencia = self.object.accion.incidencia.centro_asistencia
				mensaje = "Se ha solicitado un recurso desde el %s, que se detalla en el siguiente archivo adjunto." %(centro_asistencia.nombre) 
				email = EmailMessage('SOLICITUD DE RECURSO', mensaje , settings.EMAIL_HOST_USER ,[self.object.proveedor.correo]) 		
				email.attach_file(convertHtmlToPdf(self.object.id))
				email.send(fail_silently=False)
		else:
			if anterior_notificar_email: #true
				messages.add_message(self.request, messages.ERROR, 'El cambio de notificación por email no se ha realizado porque ya se ha notificado antes')
				self.object.notificar_email = anterior_notificar_email
				self.object.save()
				convertHtmlToPdf(self.object.id)
			else:
				# NO SEN ENVIA EL EMAIL PERO SE CREA EL REPORTE
				convertHtmlToPdf(self.object.id)
		
		# DEJAR O NO EN ESPERA
	
		if self.object.esperar != anterior_esperar:
			solicitudes = Solicitud_Recurso.objects.filter(Q(estado=True), Q(esperar=True), ~Q(id=self.object.id))
			if self.object.esperar:				
				# SI HO HAY SOLICITUDES QUE DEJEN EN ESPERA A LA INCIDENCIA 
				if not solicitudes or (self.object.accion.incidencia.estado_incidencia != ESTADO_PENDIENTE):
					# función de esperar				
					incidencia = self.object.accion.incidencia
					incidencia.caduca = None
					incidencia.estado_incidencia = ESTADO_PENDIENTE
					incidencia.save()
					#calcular duracion restante
					historial_aux = Historial_Incidencia.objects.filter(incidencia=self.object.accion.incidencia).latest('id')				
					hoy = timezone.now()				
					utilizado = hoy - historial_aux.fecha				
					restante= historial_aux.tiempo_restante - utilizado				

					historial = Historial_Incidencia(incidencia= self.object.accion.incidencia, tipo='3', fecha = datetime.now() , tiempo_restante= restante)				
					historial.save()	
			else:
				if not solicitudes :					
					incidencia = self.object.accion.incidencia
					historial_aux = Historial_Incidencia.objects.filter(incidencia=self.object.accion.incidencia).latest('id')
					hoy = timezone.now()
					incidencia.caduca = hoy + historial_aux.tiempo_restante
					incidencia.estado_incidencia = ESTADO_ABIERTA
					incidencia.save()

		return super(SolicitudUpdate, self).form_valid(form)					

	def get_success_url(self):
		try:
			return reverse('solicitudes_list', kwargs={'accion_id': self.object.accion.id, 'incidencia_id': self.object.accion.incidencia.id})
		except Exception, e:
			print e


class SolicitudDelete(DeleteView):
	model = Solicitud_Recurso
	template_name = 'accion/recurso/recurso_confirm_delete.html'	
	success_message = 'Solicitud de recurso eliminada con éxito'	

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.delete_solicitud_recurso', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.solicitud_id = kwargs['pk']
		return super(SolicitudDelete, self).dispatch(*args, **kwargs)	
					

	def delete(self, request, *args, **kwargs):			

		self.object = self.get_object()
		id_solicitud = self.object.id		

		if self.object.accion.tecnico != self.request.user:			
			messages.add_message(self.request, messages.ERROR, 'Permiso Denegado')
			return HttpResponseRedirect(reverse_lazy('solicitudes_list', kwargs={'accion_id':self.object.accion.id, 'incidencia_id':self.object.accion.incidencia.id}))
		
		if self.object.despachado:
			messages.add_message(self.request, messages.ERROR, 'No se puede eliminar. Este recurso ya se ha despachado')			
			return HttpResponseRedirect(reverse_lazy('solicitudes_list', kwargs={'accion_id':self.object.accion.id, 'incidencia_id':self.object.accion.incidencia.id}))


		solicitud = get_object_or_404(Solicitud_Recurso, pk=id_solicitud)				

		if solicitud.notificar_email:
			messages.add_message(self.request, messages.ERROR, 'No se puede eliminar porque ya se ha notificado al usuario')
		else:
			if solicitud.esperar:
				# verficar si hay otras solicitudes haciendo que espere y retomar la incidencia
				solicitudes = Solicitud_Recurso.objects.filter(Q(estado=True), Q(esperar=True), ~Q(id=self.object.id))
				if not solicitudes :					
					incidencia = self.object.accion.incidencia
					historial_aux = Historial_Incidencia.objects.filter(incidencia=self.object.accion.incidencia).latest('id')
					hoy = timezone.now()
					incidencia.caduca = hoy + historial_aux.tiempo_restante
					incidencia.estado_incidencia = ESTADO_ABIERTA
					incidencia.save()					 
					messages.add_message(self.request, messages.INFO, 'La incidencia ha iniciado nuevamente. Recuerde que la incidencia caduca %s'%formats.date_format(incidencia.caduca, "SHORT_DATETIME_FORMAT"))
			self.object.estado = False
			self.object.esperar = False
			self.object.save()		
			messages.success(self.request, self.success_message)
		return HttpResponseRedirect(reverse_lazy('solicitudes_list', kwargs={'accion_id':self.object.accion.id, 'incidencia_id':self.object.accion.incidencia.id}))



########################################
#  ENTRADA DE  SOLICITUDES DE RECURSO  #
########################################

class AccionEntradasList(ListView):
	model = Entrada_Recurso
	template_name = 'accion/accion/accion_list_entrada.html'
	context_object_name = 'entradas'

	@method_decorator(login_required)	
	def dispatch(self, *args, **kwargs):
		if permiso_incidencia_detail(self):
			return super(AccionEntradasList, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied

	def get_context_data(self, **kwargs):
		context = super(AccionEntradasList, self).get_context_data(**kwargs)		
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
		queryset = Entrada_Recurso.objects.filter(Q(estado=True), Q(solicitud_recurso__accion__incidencia_id=incidencia))		
		return queryset


class EntradaCreate(SuccessMessageMixin, CreateView):
	model = Entrada_Recurso
	template_name = 'accion/recurso/entrada_create_form.html'
	form_class = Entrada_RecursoForm
	success_message = u"Entrada de recurso se ha creado con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.add_entrada_recurso', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):		
		# self.proviene =  self.request.resolver_match.url_name

		solicitud = get_object_or_404(Solicitud_Recurso, pk= int(self.kwargs['solicitud_id']))
		self.kwargs['incidencia_id'] = solicitud.accion.incidencia.id		
		if permiso_incidencia_detail(self):
			if solicitud.accion.incidencia.es_vigente(request=self.request):	
				if solicitud.tecnico == self.request.user:
					entrada = Entrada_Recurso.objects.filter(solicitud_recurso=solicitud)
					if not entrada:													
						return super(EntradaCreate, self).dispatch(*args, **kwargs)
					else:
						messages.add_message(self.request, messages.ERROR, 'Ya se ha generado una entrada de recurso para ésta solicitud')			
						return HttpResponseRedirect(reverse_lazy('accion_list_solicitud', kwargs={'incidencia_id':solicitud.accion.incidencia.id}))
				else:
					raise PermissionDenied
			else:
				messages.add_message(self.request, messages.ERROR, 'No se puede agregar. La incidencia está cerrada')			
				return HttpResponseRedirect(reverse_lazy('accion_list_solicitud', kwargs={'incidencia_id':solicitud.accion.incidencia.id}))
		else:
			raise PermissionDenied

	def get_success_url(self):
		try:
			return reverse('accion_list_solicitud', kwargs={'incidencia_id': self.object.solicitud_recurso.accion.incidencia.id})
		except Exception, e:
			print e

	def get_context_data(self, **kwargs):
		context = super(EntradaCreate, self).get_context_data(**kwargs)				
		solicitud = get_object_or_404(Solicitud_Recurso, pk=int(self.kwargs['solicitud_id']))				
		context['solicitud'] = solicitud
		return context

	def form_valid(self, form):
		solicitud = get_object_or_404(Solicitud_Recurso, pk= int(self.kwargs['solicitud_id']))		
		self.object = form.save(commit=False)		
		self.object.solicitud_recurso = solicitud
		self.object.usuario_registra = self.request.user	
		self.object.save()		
		if self.object.solicitud_recurso.esperar:			
			self.object.solicitud_recurso.esperar = False						
			solicitudes = Solicitud_Recurso.objects.filter(Q(estado=True), Q(esperar=True), ~Q(id=self.object.solicitud_recurso.id))			
			if not solicitudes:									
				incidencia = self.object.solicitud_recurso.accion.incidencia				
				historial_aux = Historial_Incidencia.objects.filter(incidencia=self.object.solicitud_recurso.accion.incidencia).latest('id')				
				print historial_aux
				hoy = timezone.now()
				
				incidencia.caduca = hoy + historial_aux.tiempo_restante
				incidencia.estado_incidencia = ESTADO_ABIERTA
				print "entra 8"
				incidencia.save()
		
		self.object.solicitud_recurso.despachado = True
		self.object.solicitud_recurso.save()
			
		return super(EntradaCreate, self).form_valid(form)




class EntradaUpdate(SuccessMessageMixin, UpdateView):
	model = Entrada_Recurso
	template_name = 'accion/recurso/entrada_create_form.html'
	form_class = Entrada_Recurso_EditForm
	success_message = u"Entrada de recurso se ha actualizado con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.change_entrada_recurso', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):		
		entrada = get_object_or_404(Entrada_Recurso, pk= int(self.kwargs['pk']))
		self.kwargs['incidencia_id'] = entrada.solicitud_recurso.accion.incidencia.id		
		if permiso_incidencia_detail(self):			
			if entrada.solicitud_recurso.accion.incidencia.es_vigente(request=self.request):				
				if entrada.usuario_registra == self.request.user:								
					return super(EntradaUpdate, self).dispatch(*args, **kwargs)
				else:					
					raise PermissionDenied
			else:
				messages.add_message(self.request, messages.ERROR, 'No se puede actualizar. La incidencia está cerrada')			
				return HttpResponseRedirect(reverse_lazy('accion_list_entrada', kwargs={'incidencia_id':entrada.solicitud_recurso.accion.incidencia.id}))
		else:
			raise PermissionDenied

	def get_success_url(self):	
		entrada  = self.get_object()	
		try:
			return reverse('accion_list_entrada', kwargs={'incidencia_id': entrada.solicitud_recurso.accion.incidencia.id})
		except Exception, e:
			print e

	def get_context_data(self, **kwargs):
		context = super(EntradaUpdate, self).get_context_data(**kwargs)		
		entrada  = self.get_object()				
		context['solicitud'] = entrada.solicitud_recurso
		return context	


class EntradaUpdatedetail(DetailView):
	model = Entrada_Recurso
	template_name = 'accion/recurso/vista_entrada_form.html'

	@method_decorator(login_required)
	@method_decorator(permission_required('accion.add_entrada_recurso', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):			
		entrada = get_object_or_404(Entrada_Recurso, pk= int(self.kwargs['pk']))
		self.kwargs['incidencia_id'] = entrada.solicitud_recurso.accion.incidencia.id		
		if permiso_incidencia_detail(self):			
			return super(EntradaUpdatedetail, self).dispatch(*args, **kwargs)			
		else:
			raise PermissionDenied


#AGREGAR CUANDO CREE LA SOLICITUD DE INCIDENCIA
# # AGREGA LA INCIDENCIA AL HISTORIAL CON FECHAS
		# historial = Historial_Incidencia(incidencia= self.object, tipo='0', fecha = datetime.now() , tiempo_restante= None)
		# historial.save()