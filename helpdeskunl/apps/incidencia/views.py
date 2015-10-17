# -*- coding: utf-8 -*-
#REQUEST
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import HttpResponseForbidden
#MODELS
from helpdeskunl.apps.incidencia.form import *
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.home.models import *
from helpdeskunl.apps.accion.models import *

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
from django.utils import formats
from django.utils import timezone

# CONSULTAS
from django.db.models import Q

# ENCRIPTAR
import base64   

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
		querty =  self.request.POST

		try:
			for idbien in querty.pop('bien'):
				bien = Bien.objects.get(pk=int(idbien))
				self.object.bienes.add(bien)
			self.object.save()
		except Exception, e:
			print e
			
	 	administradores = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia = self.object.centro_asistencia).distinct()
	 	
	 	url = base64.encodestring(reverse_lazy('incidencia_centro_list'))

	 	for administrador in administradores:

	 		notificacion = Notificacion(remitente=self.request.user, destinatario = administrador, tipo = '0', dirigirse=url)
			notificacion.save()			
			notificacion.construir_notificacion(extra=self.object.centro_asistencia.nombre)

			if administrador.id == self.request.user.id:
				messages.add_message(self.request, messages.INFO, notificacion.mensaje)										
			else:
				notificacion.notificar()
			# ishout_client.emit(administrador.id, 'notificaciones', data = {'msg':'Se ha agregado una nueva incidencia'})		
		

		# AGREGA LA INCIDENCIA AL HISTORIAL CON FECHAS
		historial = Historial_Incidencia(incidencia= self.object, tipo='0', fecha = datetime.now() , tiempo_restante= None)
		historial.save()

		return super(IncidenciaCreate, self).form_valid(form)

# http://stackoverflow.com/questions/18434920/django-posting-a-template-value-to-a-view
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

	def get_context_data(self, **kwargs):
		context = super(IncidenciaUpdate, self).get_context_data(**kwargs)		
		bienes = self.object.bienes.all()
		context['bienes_incidencia'] = bienes
		return context

	def form_valid(self, form):
		self.object = form.save()
		querty =  self.request.POST
		self.object.bienes.clear()
		try:
			for idbien in querty.pop('bien'):
				bien = Bien.objects.get(pk=int(idbien))
				self.object.bienes.add(bien)
			self.object.save()
		except Exception, e:
			print e
		
		return super(IncidenciaUpdate, self).form_valid(form)
		

class IncidenciaDelete(DeleteView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_confirm_delete.html'	
	success_message = 'Incidencia eliminada con éxito'
	success_url = reverse_lazy('incidencia_list')

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.delete_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		self.incidencia_id = kwargs['pk']				
		return super(IncidenciaDelete, self).dispatch(*args, **kwargs)	

	def delete(self, request, *args, **kwargs):	
		self.object = self.get_object()
		id_incidencia = self.object.id
		mensaje =""
		incidencia = get_object_or_404(Incidencia, pk=id_incidencia)
		try:
			if incidencia.asignacion_incidencia_set.all():
				messages.add_message(self.request, messages.ERROR, 'No se puede eliminar el registro. '+incidencia.titulo + u' ya está siendo atendida')
				return HttpResponseRedirect(reverse_lazy('incidencia_list'))
			else:
				self.object.estado = False
				self.object.estado_incidencia = '3'
				self.object.save()
				mensaje = "ok"
				messages.success(self.request, self.success_message)
				return HttpResponseRedirect(self.get_success_url())
				# messages.add_message(self.request, messages.SUCCESS, u'Incidencia eliminada con éxito')
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
		if self.request.GET.get('criterio'):	
			criterio =	self.request.GET.get('criterio')
			
			if criterio == 'Todas':
				self.tipo = 'Todas las incidencias'
				queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user)
			if criterio == 'Estado':
				estado = self.request.GET.get('estado')
				self.tipo = 'Todas las incidencias de estado << %s >>' %(estado)
				if estado == 'Nueva':				
					queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user, estado_incidencia=ESTADO_NUEVA).distinct()
				if estado == 'Asignada':
					queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user, estado_incidencia=ESTADO_DELEGADA).distinct()
				if estado == 'Atendiendo':
					queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user, estado_incidencia=ESTADO_ABIERTA).distinct()
				if estado == 'Cerrada':
					queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user, estado_incidencia=ESTADO_ATENDIDA).distinct()
				if estado == 'Pendiente':
					queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user, estado_incidencia=ESTADO_PENDIENTE).distinct()
				if estado == 'Reaperturada':
					queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user, estado_incidencia=ESTADO_REAPERTURADA).distinct()				
			if criterio == unicode(u'Título'):
				valor = self.request.GET.get('valor')
				self.tipo = u'Incidencias de título << %s >>' %valor				
				queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user, titulo__icontains=valor)
			if criterio == 'Solicitante':
				valor = self.request.GET.get('valor')
				self.tipo = 'Incidencias para el solicitante  << %s >>' %(valor)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user), Q(solicitante__nombres__icontains=valor) | Q(solicitante__apellidos__icontains=valor))
			if criterio == unicode(u'Técnico'):

				valor = self.request.GET.get('valor')				
				self.tipo = u'Incidencias para el técnico  << %s >>' %(valor)				
				queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user) and ( Q(asignacion_incidencia__tecnico__nombres__icontains=valor) | Q(asignacion_incidencia__tecnico__apellidos__icontains=valor)))				

			if criterio == 'Prioridad':
				prioridad = self.request.GET.get('prioridad')
				self.tipo = 'Incidencias de prioridad << %s >>' %(prioridad)
				if prioridad == 'Bajo':				
					queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user), Q(prioridad_asignada=UR_BAJO))
				if prioridad == 'Normal':				
					queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user), Q(prioridad_asignada=UR_NORMAL))
				if prioridad == 'Alta':				
					queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user), Q(prioridad_asignada=UR_ALTO))		
			if criterio == unicode(u'Fecha creación'):

				fecha_desde = datetime.strptime(self.request.GET.get('fecha_desde'), "%Y-%m-%d")
				fecha_hasta = datetime.strptime(self.request.GET.get('fecha_hasta'), "%Y-%m-%d")
				self.tipo = u'Incidencias con fecha de creación << Desde: %s - Hasta: %s >>' %(self.request.GET.get('fecha_desde'),self.request.GET.get('fecha_hasta'))
				fecha_hasta += timedelta(days=1)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user), Q(creado_en__range=[fecha_desde, fecha_hasta]))				
				
			if criterio == unicode(u'Fecha asignación') :
				fecha_desde = datetime.strptime(self.request.GET.get('fecha_desde'), "%Y-%m-%d")
				fecha_hasta = datetime.strptime(self.request.GET.get('fecha_hasta'), "%Y-%m-%d")
				self.tipo = u'Incidencias con fecha de asignación << Desde: %s - Hasta: %s >>' %(self.request.GET.get('fecha_desde'),self.request.GET.get('fecha_hasta'))
				fecha_hasta += timedelta(days=1)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user), Q(fecha__range=[fecha_desde, fecha_hasta]))
			
			if criterio == 'Fecha caducidad':
				fecha_desde = datetime.strptime(self.request.GET.get('fecha_desde'), "%Y-%m-%d")
				fecha_hasta = datetime.strptime(self.request.GET.get('fecha_hasta'), "%Y-%m-%d")
				self.tipo = u'Incidencias con fecha de caducidad << Desde: %s - Hasta: %s >>' %(self.request.GET.get('fecha_desde'),self.request.GET.get('fecha_hasta'))
				fecha_hasta += timedelta(days=1)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(asignacion_incidencia__tecnico=self.request.user), Q(caduca__range=[fecha_desde, fecha_hasta]))
						
		else:			
			self.tipo = 'Todas las incidencias'
			queryset = Incidencia.objects.filter(estado=True, asignacion_incidencia__tecnico=self.request.user).distinct().order_by('-caduca')	 #order_by('asignacion_incidencia__fecha_asignacion')
		
		return queryset

	@method_decorator(login_required)
	@method_decorator(user_passes_test(es_tecnico))
	def dispatch(self, *args, **kwargs):
		return super(Incidencia_AsignadaList, self).dispatch(*args, **kwargs)


	def get_context_data(self, **kwargs):    
		context = super(Incidencia_AsignadaList, self).get_context_data(**kwargs)		
		if self.request.GET.get('cerrada'):
			context['render_div'] = "display:true"
		else:
			context['render_div'] = "display:none"
		
		context['title'] = self.tipo
		
		return context



class Incidencia_CentroList(ListView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_list_jd.html'
	context_object_name = 'incidencias'

	def get_queryset(self):
		# INCIDENCIAS AGRUPADAS POR CENTRO DE ASISTENCIA
		# queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO').distinct()
		# return queryset

		if self.request.GET.get('criterio'):	
			criterio =	self.request.GET.get('criterio')
			
			if criterio == 'Todas':
				self.tipo = 'Todas las incidencias'
				queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO')
			if criterio == 'Estado':
				estado = self.request.GET.get('estado')
				self.tipo = 'Todas las incidencias de estado << %s >>' %(estado)
				if estado == 'Nueva':				
					queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO', estado_incidencia=ESTADO_NUEVA).distinct()
				if estado == 'Asignada':
					queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO', estado_incidencia=ESTADO_DELEGADA).distinct()
				if estado == 'Atendiendo':
					queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO', estado_incidencia=ESTADO_ABIERTA).distinct()
				if estado == 'Cerrada':
					queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO', estado_incidencia=ESTADO_ATENDIDA).distinct()
				if estado == 'Pendiente':
					queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO', estado_incidencia=ESTADO_PENDIENTE).distinct()
				if estado == 'Reaperturada':
					queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO', estado_incidencia=ESTADO_REAPERTURADA).distinct()				
			if criterio == unicode(u'Título'):
				valor = self.request.GET.get('valor')
				self.tipo = u'Incidencias de título << %s >>' %valor				
				queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO', titulo__icontains=valor)
			if criterio == 'Solicitante':
				valor = self.request.GET.get('valor')
				self.tipo = 'Incidencias para el solicitante  << %s >>' %(valor)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO'), Q(solicitante__nombres__icontains=valor) | Q(solicitante__apellidos__icontains=valor))
			if criterio == unicode(u'Técnico'):

				valor = self.request.GET.get('valor')				
				self.tipo = u'Incidencias para el técnico  << %s >>' %(valor)				
				queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO') and ( Q(asignacion_incidencia__tecnico__nombres__icontains=valor) | Q(asignacion_incidencia__tecnico__apellidos__icontains=valor)))				

			if criterio == 'Prioridad':
				prioridad = self.request.GET.get('prioridad')
				self.tipo = 'Incidencias de prioridad << %s >>' %(prioridad)
				if prioridad == 'Bajo':				
					queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO'), Q(prioridad_asignada=UR_BAJO))
				if prioridad == 'Normal':				
					queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO'), Q(prioridad_asignada=UR_NORMAL))
				if prioridad == 'Alta':				
					queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO'), Q(prioridad_asignada=UR_ALTO))		
			if criterio == unicode(u'Fecha creación'):

				fecha_desde = datetime.strptime(self.request.GET.get('fecha_desde'), "%Y-%m-%d")
				fecha_hasta = datetime.strptime(self.request.GET.get('fecha_hasta'), "%Y-%m-%d")
				self.tipo = u'Incidencias con fecha de creación << Desde: %s - Hasta: %s >>' %(self.request.GET.get('fecha_desde'),self.request.GET.get('fecha_hasta'))
				fecha_hasta += timedelta(days=1)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO'), Q(creado_en__range=[fecha_desde, fecha_hasta]))				
				
			if criterio == unicode(u'Fecha asignación') :
				fecha_desde = datetime.strptime(self.request.GET.get('fecha_desde'), "%Y-%m-%d")
				fecha_hasta = datetime.strptime(self.request.GET.get('fecha_hasta'), "%Y-%m-%d")
				self.tipo = u'Incidencias con fecha de asignación << Desde: %s - Hasta: %s >>' %(self.request.GET.get('fecha_desde'),self.request.GET.get('fecha_hasta'))
				fecha_hasta += timedelta(days=1)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO'), Q(fecha__range=[fecha_desde, fecha_hasta]))
			
			if criterio == 'Fecha caducidad':
				fecha_desde = datetime.strptime(self.request.GET.get('fecha_desde'), "%Y-%m-%d")
				fecha_hasta = datetime.strptime(self.request.GET.get('fecha_hasta'), "%Y-%m-%d")
				self.tipo = u'Incidencias con fecha de caducidad << Desde: %s - Hasta: %s >>' %(self.request.GET.get('fecha_desde'),self.request.GET.get('fecha_hasta'))
				fecha_hasta += timedelta(days=1)
				queryset = Incidencia.objects.filter(Q(estado=True), Q(centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO'), Q(caduca__range=[fecha_desde, fecha_hasta]))
						
		else:			
			self.tipo = 'Todas las incidencias'
			queryset = Incidencia.objects.filter(estado=True, centro_asistencia__personal_operativo__usuario=self.request.user, centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO').distinct().order_by('-caduca')	 #order_by('asignacion_incidencia__fecha_asignacion')
		
		return queryset


	def get_context_data(self, **kwargs):    
		context = super(Incidencia_CentroList, self).get_context_data(**kwargs)		
		context['title'] = self.tipo
		
		return context
	
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
					url = base64.encodestring(reverse_lazy('incidencia_asignada_list'))
					notificacion = Notificacion(remitente=self.request.user, destinatario = tecnico, tipo = '1', dirigirse=url)					
					notificacion.save()						
					notificacion.construir_notificacion()					

					if t.tecnico.id == self.request.user.id:
						messages.add_message(self.request, messages.INFO, notificacion.mensaje)										
					else:
						notificacion.notificar()
				except Exception, e:
					print e

		# prioridad_asignada = form.cleaned_data['prioridad_asignada']
		# prioridad_solicitada = self.object.prioridad_solicitada
		
		form.save()		
		incidencia = self.object
		if incidencia.caduca == None:			
			incidencia.fecha = datetime.now()
			incidencia.ejecucion = self.object.determinar_prioridad()		
			incidencia.duracion = self.object.determinar_duracion()
			incidencia.estado_incidencia = ESTADO_DELEGADA	

		incidencia.save()
		messages.add_message(self.request, messages.SUCCESS, "Incidencia asignada con éxito")

		######
		# NOTIFICAR A LOS USUARIOS ASIGNADOS
		######		
		historial = Historial_Incidencia(incidencia= incidencia, tipo='1', fecha = datetime.now() , tiempo_restante= incidencia.duracion)
		historial.save()

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
		incidencia_aux = self.get_object()		
		if not incidencia_aux.es_vigente(self.request):			
			ctx = {'respuesta':'ok',}
			messages.add_message(self.request, messages.ERROR, 'No se puede redirigir. La incidencia está cerrada')										
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	
		if incidencia_aux.diagnostico_inicial_set.all():			
			ctx = {'respuesta':'ok',}
			messages.add_message(self.request, messages.ERROR, 'No se puede redirigir la incidencia')										
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	
	 	incidencia = form.save()		
		incidencia.prioridad_asignada = ''
		incidencia.estado_incidencia = '0'
		incidencia.nivel = '0'
		asignaciones = incidencia.asignacion_incidencia_set.all()

		for asignacion in asignaciones:
			# NOTIFICAR A LOS USUARIOS QUE FUERON ASIGNADOS
			url = base64.encodestring(reverse_lazy('incidencia_asignada_list'))	 	
			notificacion = Notificacion(remitente=self.request.user, destinatario = asignacion.tecnico, tipo = '4', dirigirse=url)	
			notificacion.save()
			notificacion.construir_notificacion(extra=self.object.titulo)

			if asignacion.tecnico.id == self.request.user.id:
				messages.add_message(self.request, messages.INFO, notificacion.mensaje)										
			else:
				notificacion.notificar()

		asignaciones.delete()				
		incidencia.servicio = None
		incidencia.ejecucion = None
		incidencia.duracion = None
		incidencia.caduca = None
		incidencia.fecha = None
		incidencia.save()

		administradores = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia = incidencia.centro_asistencia).distinct()
	 	for administrador in administradores:
	 		url = base64.encodestring(reverse_lazy('incidencia_centro_list'))	
	 		notificacion = Notificacion(remitente=self.request.user, destinatario = administrador, tipo = '2', dirigirse=url)
			notificacion.save()			
			notificacion.construir_notificacion(extra=self.object.centro_asistencia.nombre)

			if administrador.id == self.request.user.id:
				messages.add_message(self.request, messages.INFO, notificacion.mensaje)										
			else:
				notificacion.notificar()

		messages.add_message(self.request, messages.SUCCESS, "La incidencia se ha redirigido exitosamente")

		if self.request.is_ajax():	 			 		
	 		ctx = {'respuesta':'ok', 'id':incidencia.id,}
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
	 	else:			
			return super(RedirigirIncidencia, self).form_valid(form)

class IncidenciaCompleteUpdate(SuccessMessageMixin, UpdateView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_update_form_admin.html'
	form_class = IncidenciaCompleteForm
	success_message = u"%(titulo)s se ha actualizado con éxito"

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
				url = base64.encodestring(reverse_lazy('incidencia_asignada_list'))	
				notificacion = Notificacion(remitente=self.request.user, destinatario = asignacion.tecnico, tipo = '3', dirigirse=url)					
				notificacion.save()						
				notificacion.construir_notificacion(extra=str(incidencia_test.titulo))

				if asignacion.tecnico.id == self.request.user.id:
					messages.add_message(self.request, messages.INFO, notificacion.mensaje)	
				else:
					notificacion.notificar()

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

				url = base64.encodestring(reverse_lazy('incidencia_asignada_list'))	
				notificacion = Notificacion(remitente=self.request.user, destinatario = tecnico, tipo = '1', dirigirse=url)					
				notificacion.save()						
				notificacion.construir_notificacion()

				if tecnico.id == self.request.user.id:
					messages.add_message(self.request, messages.INFO, notificacion.mensaje)	
				else:
					notificacion.notificar()

		querty =  self.request.POST
		self.object.bienes.clear()
		try:
			for idbien in querty.pop('bien'):
				bien = Bien.objects.get(pk=int(idbien))
				self.object.bienes.add(bien)			
		except Exception, e:
			print e

		incidencia = self.object
		self.object.ejecucion = self.object.determinar_prioridad()		
		self.object.duracion = self.object.determinar_duracion()		
		self.object.save()

		messages.add_message(self.request, messages.SUCCESS, self.object.titulo + u" se ha actualizado con éxito")	
		# return super(IncidenciaCompleteUpdate, self).form_valid(form)
		return super(ModelFormMixin, self).form_valid(form)		

	def get_success_url(self):
		try:
			return reverse('incidencia_detail', kwargs={'pk': self.object.id})
		except Exception, e:
			print e
	
	def get_context_data(self, **kwargs):
		context = super(IncidenciaCompleteUpdate, self).get_context_data(**kwargs)		
		bienes = self.object.bienes.all()
		context['bienes_incidencia'] = bienes
		return context

class Atender_Incidencia_Update(DeleteView):
	model = Incidencia
	template_name = 'incidencia/incidencia/atender_incidencia.html'

	@method_decorator(login_required)
	@method_decorator(user_passes_test(es_tecnico))
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))	
	def dispatch(self, *args, **kwargs):		
		self.incidencia_id = kwargs['pk']		
		
		if permiso_incidencia_detail(self):
			return super(Atender_Incidencia_Update, self).dispatch(*args, **kwargs)
		else:
			raise PermissionDenied

	def delete(self, request, *args, **kwargs):	
		incidencia = Incidencia.objects.get(pk=int(self.incidencia_id))
		hoy = timezone.now()		
		fecha_apertura = incidencia.fecha + incidencia.apertura_maxima
		
		if fecha_apertura<hoy:
			messages.add_message(self.request, messages.ERROR, 'El tiempo de apertura ha vencido')			
			return HttpResponseRedirect(reverse_lazy('incidencia_asignada_list'))	

		self.object = self.get_object()
		incidencia = get_object_or_404(Incidencia, pk=self.object.id)
		incidencia.caduca = self.object.calcular_caducidad()		
		incidencia.estado_incidencia = ESTADO_ABIERTA	
		incidencia.save()
		
		# LISTA DE APERTURA DE INCIDENCIAS
		aperturas = incidencia.apertura_incidencia_set.all()
		
		if not aperturas:			
			historial = Historial_Incidencia(incidencia= incidencia, tipo='2', fecha = timezone.now() , tiempo_restante= incidencia.duracion)
			apertura = Apertura_Incidencia(incidencia=incidencia, duracion = incidencia.duracion, usuario= self.request.user, tipo=PRIMERA_APERTURA ,observacion='Primera apertura')
		else:
			historial = Historial_Incidencia(incidencia= incidencia, tipo='7', fecha = timezone.now() , tiempo_restante= incidencia.duracion)
			apertura = Apertura_Incidencia(incidencia=incidencia, duracion = incidencia.duracion, tipo=REAPERTURA , usuario= self.request.user, observacion='Reapertura')

		historial.save()
		apertura.save()
		messages.add_message(self.request, messages.SUCCESS, u"%s, se ha aperturado con éxito. Recuerde que la incidencia caduca %s" %(incidencia.titulo, formats.date_format(incidencia.caduca, "SHORT_DATETIME_FORMAT")))		
		return HttpResponseRedirect(reverse_lazy('incidencia_asignada_list'))		



class Incidencia_RecordatorioList(ListView):
	model = Incidencia
	template_name = 'incidencia/incidencia/recordatorio.html'
	context_object_name = 'incidencias'

	def get_queryset(self):		
		queryset = Incidencia.objects.filter(estado=True, caduca__isnull=False , estado_incidencia='2',asignacion_incidencia__tecnico=self.request.user).distinct().order_by('-caduca')	 #order_by('asignacion_incidencia__fecha_asignacion')		
		new_query = list()		
		for incidencia in queryset:
			duracion = incidencia.duracion			
			caduca = incidencia.caduca			
			duracion_aux = duracion/4			
			fecha_recordar = caduca-duracion_aux			
			# print "(%s - %s / %s /%s)" %(duracion_aux, fecha_recordar, caduca, incidencia.titulo)
			hoy = timezone.now()			
			if fecha_recordar<hoy:				
				new_query.append(incidencia)		

		return new_query

	@method_decorator(login_required)
	@method_decorator(user_passes_test(es_tecnico))
	def dispatch(self, *args, **kwargs):
		return super(Incidencia_RecordatorioList, self).dispatch(*args, **kwargs)

##########################################
#           CIERRE DE INCIDENCIA         #
##########################################
class Cierre_Incidencia_Create(SuccessMessageMixin, CreateView):
	model = Cierre_Incidencia	
	template_name = 'incidencia/incidencia/cierre.html'
	form_class = Cierre_IncidenciaForm	
	success_message = u"Incidencia cerrada con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.add_cierre_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(Cierre_Incidencia_Create, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		if self.request.is_ajax():
			incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))				
			if incidencia.es_vigente(request=self.request):
				jefes_departamento = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia=incidencia.centro_asistencia)
				if incidencia.accion_set.all() or self.request.user in jefes_departamento:
					solicitudes = Solicitud_Recurso.objects.filter(Q(estado=True), Q(esperar=True), Q(accion__incidencia=incidencia))
					if not solicitudes:
						if incidencia.estado_incidencia!=ESTADO_ATENDIDA:
							self.object = form.save(commit=False)				
							incidencia.estado_incidencia = ESTADO_ATENDIDA
							incidencia.save()
							self.object.tipo = CIERRE_MANUAL
							self.object.incidencia = incidencia		
							self.object.usuario = self.request.user		
							asesores = Perfil.asesores_tecnicos.filter(personal_operativo__centro_asistencia=incidencia.centro_asistencia)
							if self.request.user in asesores:
								self.object.cerrado_tecnico = True
							else:
								self.object.cerrado_tecnico = False
			
							apertura = Apertura_Incidencia.objects.filter(incidencia=incidencia).latest('id')
							self.object.apertura_incidencia = apertura
							self.object.save()		
							messages.add_message(self.request, messages.SUCCESS, 'Incidencia cerrada con éxito')				

							# CORREGIR
							url = base64.encodestring(reverse_lazy('incidencia_centro_list'))	
							# 

							notificacion = Notificacion(remitente=self.request.user, destinatario = self.object.incidencia.solicitante, tipo = '12', dirigirse=url)
							notificacion.save()			
							notificacion.construir_notificacion(extra=self.object.incidencia.titulo)

							if self.object.incidencia.solicitante.id == self.request.user.id:
								messages.add_message(self.request, messages.INFO, notificacion.mensaje)
							else:
								notificacion.notificar()
						else:
							messages.add_message(self.request, messages.ERROR, 'No se puede cerrar. La incidencia ya está cerrada')				
					else:
						messages.add_message(self.request, messages.ERROR, 'No se puede cerrar. Hay solicitudes de recurso pendientes')			
				else:
					messages.add_message(self.request, messages.ERROR, 'No se puede cerrar. No se ha realizado acciones para ésta incidencia')			
			else:			
				messages.add_message(self.request, messages.ERROR, 'No se puede cerrar. La incidencia ya está cerrada')				
			ctx = {'respuesta':'cerrar',}
		 	return HttpResponse(json.dumps(ctx),content_type="application/json")
		else:
			return HttpResponseForbidden()

	def get_success_url(self):		
		return reverse('accion_list', kwargs={'incidencia_id': self.object.incidencia.id})

	def get_context_data(self, **kwargs):
		ctx = super(Cierre_Incidencia_Create, self).get_context_data(**kwargs)
		ctx['incidencia'] = self.kwargs['incidencia_id']
		return ctx


##########################################
#           REABRIR INCIDENCIA          #
##########################################
class Reabrir_Incidencia_Create(SuccessMessageMixin, UpdateView):
	model = Incidencia	
	template_name = 'incidencia/incidencia/despacho_reapertura.html'
	form_class = Despacho_ReaperturaIncidenciaForm	
	success_message = u"Incidencia reaperturada con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))
	@method_decorator(user_passes_test(es_jefe))
	def dispatch(self, *args, **kwargs):
		return super(Reabrir_Incidencia_Create, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		self.object = self.get_object()
		self.object = form.save()
		if self.object.estado_incidencia==ESTADO_ATENDIDA:			
			try:
				solicitud = Solicitud_Reapertura_Incidencia.objects.get(incidencia = self.object, despachado = False)
			except Solicitud_Reapertura_Incidencia.DoesNotExist:
				solicitud = None

			if solicitud:
				porcentaje = form.cleaned_data['porcentaje']		
				apertura = get_object_or_404(Apertura_Incidencia, incidencia=self.object, tipo=PRIMERA_APERTURA)
				self.object.duracion = apertura.duracion/int(porcentaje)
				self.object.fecha = datetime.now()
				self.object.estado_incidencia = ESTADO_REAPERTURADA
				self.object.caduca = None			
				
				solicitud.usuario_despacha = self.request.user
				solicitud.fecha_despacha = datetime.now()
				solicitud.despachado = True
				solicitud.porcentaje_despacha = porcentaje
				solicitud.duracion_despacha = self.object.duracion
				self.object.save()			
				solicitud.save()

				administradores = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia = self.object.centro_asistencia).distinct()
			 	for administrador in administradores:
			 		
			 		url = base64.encodestring(reverse_lazy('incidencia_asignada_list'))	

			 		notificacion = Notificacion(remitente=self.request.user, destinatario = administrador, tipo = '9',dirigirse=url)
					notificacion.save()			
					notificacion.construir_notificacion()

					if administrador.id == self.request.user.id:
						messages.add_message(self.request, messages.INFO, notificacion.mensaje)
					else:
						notificacion.notificar()

				# NOTIFICAR AL SOLICITANTE
				# CORREGIR - AGREGAR AL DETAIL DE INCIDENCIA DEL USUARIO FINAAL
				url = base64.encodestring(reverse_lazy('incidencia_asignada_list'))	
				# 
				notificacion = Notificacion(remitente=self.request.user, destinatario = self.object.solicitante, tipo = '13', dirigirse=url)
				notificacion.save()			
				notificacion.construir_notificacion(extra=self.object.titulo)

				if self.object.solicitante.id == self.request.user.id:
					messages.add_message(self.request, messages.INFO, notificacion.mensaje)
				else:
					notificacion.notificar()

				messages.add_message(self.request, messages.SUCCESS, 'Solicitud reaperturada con éxito')

				# SI TIENE SOLICITUDES PENDIENTES -- POR VERIFICAR
				solicitudes_recurso = Solicitud_Recurso.objects.filter(Q(estado=True), Q(esperar=True), Q(accion__incidencia=self.object))
				if solicitudes_recurso:
					historial_aux = Historial_Incidencia.objects.filter(incidencia=self.object).latest('id')
					historial_aux.tiempo_restante = self.object.duracion
					historial_aux.save()

			else:
				messages.add_message(self.request, messages.ERROR, 'No es posible reabrir, no existe una solicitud de reapertura')
		else:
			messages.add_message(self.request, messages.ERROR, 'No es posible reabrir, la incidencia no está cerrada')				
		ctx = {'respuesta':'cerrar',}	
	 	return HttpResponse(json.dumps(ctx),content_type="application/json")
		

class Solicitud_Reapertura_Create(SuccessMessageMixin, CreateView):
	model = Solicitud_Reapertura_Incidencia	
	template_name = 'incidencia/solicitud/solicitud_reapertura.html'
	form_class = Solicitud_ReaperturaForm	
	success_message = u"Solicitud de reapertura creada con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.add_solicitud_reapertura', raise_exception=permission_required))	
	@method_decorator(user_passes_test(es_tecnico))
	def dispatch(self, *args, **kwargs):
		return super(Solicitud_Reapertura_Create, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		if self.request.is_ajax():
			incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))
			solicitud = Solicitud_Reapertura_Incidencia.objects.filter(incidencia = incidencia, despachado = False)
			if solicitud:				
				messages.add_message(self.request, messages.ERROR, 'Ya ha se ha solicitado una reapertura con anterioridad')
				ctx = {'respuesta':'cerrar',}	
	 			return HttpResponse(json.dumps(ctx),content_type="application/json")
			
			self.object = form.save(commit=False)			
			self.object.incidencia = incidencia
			self.object.usuario = self.request.user
			self.object.save()
			messages.add_message(self.request, messages.SUCCESS, 'Solicitud de reapertura creada con éxito')

			administradores = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia = self.object.incidencia.centro_asistencia).distinct()
		 	for administrador in administradores:

		 		url = base64.encodestring(reverse_lazy('solicitud_reaperturar_list'))	
		 		
		 		notificacion = Notificacion(remitente=self.request.user, destinatario = administrador, tipo = '8', dirigirse=url)
				notificacion.save()			
				notificacion.construir_notificacion()

				if administrador.id == self.request.user.id:
					messages.add_message(self.request, messages.INFO, notificacion.mensaje)										
				else:
					notificacion.notificar()

			ctx = {'respuesta':'cerrar',}	
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
		else:
			return HttpResponseForbidden()

	def get_context_data(self, **kwargs):
		ctx = super(Solicitud_Reapertura_Create, self).get_context_data(**kwargs)
		ctx['incidencia'] = self.kwargs['incidencia_id']
		return ctx

class Solicitud_Extender_TiempoCreate(SuccessMessageMixin, CreateView):
	model = Solicitud_Extender_Tiempo	
	template_name = 'incidencia/solicitud/solicitud_extender.html'
	form_class = Solicitud_Extender_TiempoForm	
	success_message = u"Solicitud creada con éxito"

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.add_solicitud_extender_tiempo', raise_exception=permission_required))	
	@method_decorator(user_passes_test(es_tecnico))
	def dispatch(self, *args, **kwargs):
		return super(Solicitud_Extender_TiempoCreate, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(Solicitud_Extender_TiempoCreate, self).get_context_data(**kwargs)
		ctx['incidencia'] = self.kwargs['incidencia_id']
		return ctx

	def form_valid(self, form):
		if self.request.is_ajax():
			incidencia = get_object_or_404(Incidencia, pk=int(self.kwargs['incidencia_id']))
			solicitud = Solicitud_Extender_Tiempo.objects.filter(incidencia = incidencia, despachado = False)
			if solicitud:				
				messages.add_message(self.request, messages.ERROR, 'Ya ha se ha solicitado con anterioridad')
				ctx = {'respuesta':'cerrar',}	
	 			return HttpResponse(json.dumps(ctx),content_type="application/json")
			
			self.object = form.save(commit=False)
			self.object.incidencia = incidencia
			self.object.usuario = self.request.user
			self.object.fecha_anterior = incidencia.fecha
			self.object.save()

			messages.add_message(self.request, messages.SUCCESS, 'Solicitud creada con éxito')

			administradores = Perfil.jefes_departamento.filter(personal_operativo__centro_asistencia = self.object.incidencia.centro_asistencia).distinct()
		 	for administrador in administradores:
		 		
		 		url = base64.encodestring(reverse_lazy('solicitud_extender_list'))	
		 		notificacion = Notificacion(remitente=self.request.user, destinatario = administrador, tipo = '10', dirigirse=url)
				notificacion.save()			
				notificacion.construir_notificacion()

				if administrador.id == self.request.user.id:
					messages.add_message(self.request, messages.INFO, notificacion.mensaje)										
				else:
					notificacion.notificar()

			ctx = {'respuesta':'cerrar',}	
	 		return HttpResponse(json.dumps(ctx),content_type="application/json")
		else:
			return HttpResponseForbidden()


class Solicitud_ExtenderList(ListView):
	model = Solicitud_Extender_Tiempo
	template_name = 'incidencia/solicitud/solicitud_extender_list.html'
	context_object_name = 'solicitudes'

	def get_queryset(self):
		queryset = Solicitud_Extender_Tiempo.objects.filter(estado=True, incidencia__centro_asistencia__personal_operativo__usuario=self.request.user, incidencia__centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO').distinct()		
		return queryset

	@method_decorator(login_required)	
	@method_decorator(user_passes_test(es_jefe))
	def dispatch(self, *args, **kwargs):
		return super(Solicitud_ExtenderList, self).dispatch(*args, **kwargs)

class Solicitud_ReaperturarList(ListView):
	model = Solicitud_Reapertura_Incidencia
	template_name = 'incidencia/solicitud/solicitud_reaperturar_list.html'
	context_object_name = 'solicitudes'

	def get_queryset(self):
		queryset = Solicitud_Reapertura_Incidencia.objects.filter(estado=True, incidencia__centro_asistencia__personal_operativo__usuario=self.request.user, incidencia__centro_asistencia__personal_operativo__grupo__name='JEFE DEPARTAMENTO').distinct()		
		return queryset

	@method_decorator(login_required)	
	@method_decorator(user_passes_test(es_jefe))
	def dispatch(self, *args, **kwargs):
		return super(Solicitud_ReaperturarList, self).dispatch(*args, **kwargs)


class Atender_Solicitud_Extender_Tiempo(DeleteView):
	model = Solicitud_Extender_Tiempo
	template_name = 'incidencia/solicitud/solicitud_extender_confirm.html'	
	success_message = 'Extendido con éxito'	

	@method_decorator(login_required)	
	@method_decorator(user_passes_test(es_jefe))
	@method_decorator(permission_required('incidencia.change_solicitud_extender_tiempo', raise_exception=permission_required))	
	def dispatch(self, *args, **kwargs):		
		self.solicitud_extender_tiempo = kwargs['pk']				
		return super(Atender_Solicitud_Extender_Tiempo, self).dispatch(*args, **kwargs)		

	def delete(self, request, *args, **kwargs):	
		self.object = self.get_object()
		self.object.despachado = True
		self.object.usuario_despacha = request.user
		incidencia = self.object.incidencia
		incidencia.fecha = timezone.now()		
		incidencia.save()
		self.object.save()
		messages.add_message(self.request, messages.SUCCESS, 'Tiempo extendido con éxito')			
		return HttpResponseRedirect(reverse_lazy('solicitud_extender_list'))		
	




##############################
#   BIENES INSTITUCIONALES   #
##############################

# class BienesImportList(ListView):
# 	model = Bienes
# 	template_name = 'incidencia/bien/buscar_bienes.html'
# 	context_object_name = 'bienes'

# 	def get_queryset(self):		
# 		queryset = Bien.objects.filter(estado=True, creado_por=self.request.user.id).order_by('-fecha')		
# 		return queryset

# 	@method_decorator(login_required)	
# 	def dispatch(self, *args, **kwargs):
# 		return super(BienesImportList, self).dispatch(*args, **kwargs)


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

