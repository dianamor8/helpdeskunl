# -*- coding: utf-8 -*-
#REQUEST
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import json
#MODELS
from helpdeskunl.apps.incidencia.form import *
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.home.models import *

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

# Create your views here.
# def add_dependencia_view(request):
# 	if request.method == 'POST':
# 		form_dependencia = Dependencia_Form(request.POST)
# 		if form_dependencia.is_valid():			
# 			dependencia = form_dependencia.save()
# 			mensaje = 'Información guardada satisfactoriamente.'
# 			form_dependencia = Dependencia_Form()			
# 		else:
# 			mensaje = 'La información contiene datos incorrectos.'
# 		ctx = {'form':form_dependencia, 'mensaje':mensaje}
# 		return render (request, 'incidencia/dependencia/add_dependencia.html', ctx)
# 	else:		
# 		mensaje = 'Nueva dependencia'
# 		form_dependencia = Dependencia_Form()	
# 		ctx = {'form':form_dependencia, 'mensaje':mensaje}		
# 		return render (request, 'incidencia/dependencia/add_dependencia.html', ctx)

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
	incidencia = get_object_or_404(Incidencia, pk=self.incidencia_id)
	
	asesores = Perfil.asesores_tecnicos.filter(personal_operativo__centro_asistencia=incidencia.centro_asistencia)
	jefes_departamento = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia=incidencia.centro_asistencia)
	respuesta = False
	
	if self.request.user in asesores:
		respuesta = True		
	if self.request.user in jefes_departamento:
		respuesta = True
	if self.request.user == incidencia.solicitante:
		respuesta = True

	return respuesta


##############################
#         INCIDENCIA         #
##############################
class IncidenciaList(ListView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_list.html'
	context_object_name = 'incidencias'

	def get_queryset(self):		
		queryset = Incidencia.objects.filter(estado=True, creado_por=self.request.user.id).order_by('-fecha')		
		return queryset

	@method_decorator(login_required)	
	def dispatch(self, *args, **kwargs):
		return super(IncidenciaList, self).dispatch(*args, **kwargs)


	# PARA UN LISTVIEW  PERSONALIZADO SEGUN SE ESCOJA
	# http://stackoverflow.com/questions/22902457/django-listview-customising-queryset		

class IncidenciaCreate(SuccessMessageMixin, CreateView):
	model = Incidencia	
	template_name = 'incidencia/incidencia/incidencia_create_form.html'
	form_class = IncidenciaForm
	success_url = reverse_lazy('incidencia_list')
	success_message = u"%(titulo)s se ha creado con éxito."

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.add_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):		
		return super(IncidenciaCreate, self).dispatch(*args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(IncidenciaCreate, self).get_form_kwargs()
		kwargs.update({'my_user': self.request.user})
		return kwargs
	
	def form_valid(self, form):		
		self.object = form.save()
	 	administradores = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia = self.object.centro_asistencia).distinct()
	 	for administrador in administradores:
	 		notificacion = Notificacion(remitente=self.request.user, destinatario = administrador, tipo = '0')
			notificacion.save()			
			notificacion.construir_notificacion()
			notificacion.notificar()	 		
			# ishout_client.emit(administrador.id, 'notificaciones', data = {'msg':'Se ha agregado una nueva incidencia'})		
		return super(IncidenciaCreate, self).form_valid(form)

	# def get_context_data(self, **kwargs):
	# 	context = super(IncidenciaCreate, self).get_context_data(**kwargs)
	# 	if self.request.POST:
	# 		context['formset'] = BienFormSet(self.request.POST)
	# 	else:
	# 		context['formset'] = BienFormSet()
	# 	return context

class IncidenciaUpdate(SuccessMessageMixin, UpdateView):
	model = Incidencia	
	template_name = 'incidencia/incidencia/incidencia_create_form.html'
	form_class = IncidenciaForm
	success_url = reverse_lazy('incidencia_list')
	success_message = u"%(titulo)s se ha actualizado con éxito."

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.incidencia_id = kwargs['pk']
		if soy_propietario_incidencia(self):
			incidencia = get_object_or_404(Incidencia, pk=self.incidencia_id)
			if incidencia.estado_incidencia == '3':
				messages.add_message(self.request, messages.ERROR, incidencia.titulo +' ha caducado')				
				return HttpResponseRedirect(reverse_lazy('incidencia_list'))
			else:
				if incidencia.asignacion_incidencia_set.all():
					messages.add_message(self.request, messages.ERROR, 'No se puede actualizar el registro. '+incidencia.titulo + u' ya está siendo atendida')				
					return HttpResponseRedirect(reverse_lazy('incidencia_list'))
				else:
					return super(IncidenciaUpdate, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied
	
	def get_form_kwargs(self):
		kwargs = super(IncidenciaUpdate, self).get_form_kwargs()
		kwargs.update({'my_user': self.request.user})
		return kwargs

class IncidenciaDelete(DeleteView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_confirm_delete.html'
	
	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.delete_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(IncidenciaDelete, self).dispatch(*args, **kwargs)	

	def delete(self, request, *args, **kwargs):	
		self.object = self.get_object()
		id_incidencia = self.object.id
		mensaje =""
		try:
			self.object.delete()
			mensaje = "ok"			

		except IntegrityError:
			mensaje = 'NO ES POSIBLE BORRAR, INCIDENCIA EN CURSO'			

		ctx = {'respuesta': mensaje, 'id':id_incidencia,}
		return HttpResponse(json.dumps(ctx), content_type='application/json')

class Incidencia_AsignadaList(ListView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_list_at.html'
	context_object_name = 'incidencias'

	def get_queryset(self):		
		# CONSULTA PARA INCIDENCIAS ASIGNADAS PARA MI
		queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user).distinct().order_by('-caduca')	 #order_by('asignacion_incidencia__fecha_asignacion')
		return queryset

	@method_decorator(login_required)
	@method_decorator(user_passes_test(es_tecnico))
	def dispatch(self, *args, **kwargs):
		return super(Incidencia_AsignadaList, self).dispatch(*args, **kwargs)


class Incidencia_CentroList(ListView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_list_jd.html'
	context_object_name = 'incidencias'

	def get_queryset(self):
		# INCIDENCIAS AGRUPADAS POR CENTRO DE ASISTENCIA
		queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO').distinct()
		return queryset
	
	@method_decorator(login_required)
	@method_decorator(user_passes_test(es_jefe))
	def dispatch(self, *args, **kwargs):
		return super(Incidencia_CentroList, self).dispatch(*args, **kwargs)

class Incidencia_DetailView(DetailView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_detail.html'

	def get_context_data(self, **kwargs):    
		context = super(Incidencia_DetailView, self).get_context_data(**kwargs)
		asignacion = Asignacion_Incidencia.objects.filter(incidencia=self.object)		
		administradores = Perfil.jefes_departamento.all()
		bandera = False
		if self.request.user in administradores:
			bandera = True
			if asignacion:
				bandera = False
		context['asignar_incidencia'] = bandera
		
		if self.request.user in administradores:
			context['render_div'] = "display:true"
		else:
			context['render_div'] = "display:none"
		
		return context

	@method_decorator(login_required)
	# PERMISOS ADD ACCION, CHANGE INCIDENCIA
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))	
	def dispatch(self, *args, **kwargs):
		self.incidencia_id = kwargs['pk']
		if permiso_incidencia_detail(self):
			return super(Incidencia_DetailView, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied




class AsignarIncidencia(UpdateView):
	model = Incidencia	
	template_name = 'incidencia/incidencia/asignacion.html'
	form_class = AsignacionForm

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):		
		return super(AsignarIncidencia, self).dispatch(*args, **kwargs)
	
	def get_form_kwargs(self):
		kwargs = super(AsignarIncidencia, self).get_form_kwargs()		
		perfiles = Perfil.objects.filter(personal_operativo__centro_asistencia__id=self.object.centro_asistencia.id, personal_operativo__grupo__name='ASESOR TECNICO').distinct()		
		servicios = Servicio.objects.filter(centro__id=self.object.centro_asistencia.id)
		kwargs.update({'perfiles': perfiles})
		kwargs.update({'servicios': servicios})
		return kwargs

	def form_valid(self, form):
		incidencia = self.object
		tecnicos = form.cleaned_data['tecnicos']

		asignaciones = incidencia.asignacion_incidencia_set.all()
		tecnicos_existentes = list()
		
		for asignacion in asignaciones:
			tecnicos_existentes.append(asignacion.tecnico)

		for tecnico in tecnicos:			
			if tecnico not in tecnicos_existentes:
				try:
					t = Asignacion_Incidencia()
					t.incidencia= incidencia
					t.tecnico = tecnico
					t.administrador= self.request.user
					t.observacion='Creado por asignación'
					t.save()
					
		
					notificacion = Notificacion(remitente=self.request.user, destinatario = tecnico, tipo = '1')					
					notificacion.save()						
					notificacion.construir_notificacion()										
					notificacion.notificar()					
					
				except Exception, e:
					print e

		# prioridad_asignada = form.cleaned_data['prioridad_asignada']
		# prioridad_solicitada = self.object.prioridad_solicitada
		
		form.save()		
		incidencia = self.object
		incidencia.ejecucion = self.object.determinar_prioridad()		
		incidencia.duracion = self.object.determinar_duracion()
		incidencia.estado_incidencia = ESTADO_ABIERTA
		incidencia.caduca = self.object.calcular_caducidad()
		incidencia.save()

		######
		# NOTIFICAR A LOS USUARIOS ASIGNADOS
		######

		if self.request.is_ajax():	 			 		
	 		ctx = {'respuesta':'ok', 'id':incidencia.id,}
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	else:
			return super(AsignarIncidencia, self).form_valid(form)
	
	def get_success_url(self):
		try:
			return reverse('incidencia_detail', kwargs={'pk': self.object.id})
		except Exception, e:
			print e
		

class RedirigirIncidencia(UpdateView):
	model = Incidencia	
	template_name = 'incidencia/incidencia/redirigir.html'
	form_class = RedirigirIncidenciaForm

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))
	@method_decorator(user_passes_test(es_jefe))
	def dispatch(self, *args, **kwargs):		
		return super(RedirigirIncidencia, self).dispatch(*args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(RedirigirIncidencia, self).get_form_kwargs()
		kwargs.update({'centro_asistencia': self.object.centro_asistencia})
		return kwargs

	def form_valid(self, form):
		incidencia = form.save()		
		incidencia.prioridad_asignada = ''
		incidencia.estado_incidencia = '0'
		incidencia.nivel = '0'
		asignaciones = incidencia.asignacion_incidencia_set.all()
		asignaciones.delete()				
		incidencia.servicio = None
		incidencia.ejecucion = None
		incidencia.duracion = None
		incidencia.caduca = None
		incidencia.save()

		administradores = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia = incidencia.centro_asistencia).distinct()
	 	for administrador in administradores:
	 		notificacion = Notificacion(remitente=self.request.user, destinatario = administrador, tipo = '2')
			notificacion.save()			
			notificacion.construir_notificacion()
			notificacion.notificar()

		if self.request.is_ajax():	 			 		
	 		ctx = {'respuesta':'ok', 'id':incidencia.id,}
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	else:			
			return super(RedirigirIncidencia, self).form_valid(form)

class IncidenciaCompleteUpdate(UpdateView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_update_form_admin.html'
	form_class = IncidenciaCompleteForm	

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.incidencia_id = kwargs['pk']
		incidencia = get_object_or_404(Incidencia, pk=self.incidencia_id)
		jefes_departamento = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia=incidencia.centro_asistencia)			
		if self.request.user in jefes_departamento:	
			return super(IncidenciaCompleteUpdate, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied
	
	def get_form_kwargs(self):
		kwargs = super(IncidenciaCompleteUpdate, self).get_form_kwargs()
		kwargs.update({'my_user': self.object.solicitante})
		perfiles = Perfil.objects.filter(personal_operativo__centro_asistencia__id=self.object.centro_asistencia.id, personal_operativo__grupo__name='ASESOR TECNICO').distinct()		
		servicios = Servicio.objects.filter(centro__id=self.object.centro_asistencia.id)
		kwargs.update({'perfiles': perfiles})
		kwargs.update({'servicios': servicios})
		return kwargs


	def form_valid(self, form):
		self.object = form.save(commit=False)
		tecnicos = form.cleaned_data['tecnicos']
		asignaciones = self.object.asignacion_incidencia_set.all()
		incidencia_test = get_object_or_404(Incidencia, pk=self.object.id)
		tecnicos_existentes = list()		
		
		for asignacion in asignaciones:			
			if asignacion.tecnico not in tecnicos:								
				asignacion.delete()				
			else:
				tecnicos_existentes.append(asignacion.tecnico)		

		for tecnico in tecnicos: #TECNICOS SELECCIONADOS	
			if tecnico not in tecnicos_existentes:				
				t = Asignacion_Incidencia()
				t.incidencia= incidencia_test
				t.tecnico = tecnico
				t.administrador= self.request.user
				t.observacion='Creado por actualización'
				t.save()

				notificacion = Notificacion(remitente=self.request.user, destinatario = tecnico, tipo = '1')					
				notificacion.save()						
				notificacion.construir_notificacion()										
				notificacion.notificar()
				
		incidencia = self.object
		self.object.ejecucion = self.object.determinar_prioridad()		
		self.object.duracion = self.object.determinar_duracion()		
		self.object.caduca = self.object.calcular_caducidad()		
		self.object.save()		
		# return super(IncidenciaCompleteUpdate, self).form_valid(form)
		return super(ModelFormMixin, self).form_valid(form)		

	def get_success_url(self):
		try:
			return reverse('incidencia_detail', kwargs={'pk': self.object.id})
		except Exception, e:
			print e

##############################
#   BIENES INSTITUCIONALES   #
##############################

class BienCreate(CreateView):	
	template_name = 'incidencia/bien/bien_edit_form.html'
	form_class = BienForm

	def get_context_data(self, **kwargs):
		context = super(BienCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = Caracteristica_BienFormSet(self.request.POST)
		else:
			context['formset'] = Caracteristica_BienFormSet()
		return context