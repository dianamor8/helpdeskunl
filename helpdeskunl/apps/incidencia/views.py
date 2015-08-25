# -*- coding: utf-8 -*-
#REQUEST
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
import json
#MODELS
from helpdeskunl.apps.incidencia.form import *
from helpdeskunl.apps.incidencia.models import *
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
# METODOS DECORADORES
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
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
#         INCIDENCIA         #
##############################
class IncidenciaList(ListView):
	model = Incidencia
	template_name = 'incidencia/incidencia/incidencia_list.html'
	context_object_name = 'incidencias'

	def get_queryset(self):		
		queryset = Incidencia.objects.filter(estado=True, creado_por=self.request.user.id).order_by('fecha')
		return queryset

	@method_decorator(login_required)	
	def dispatch(self, *args, **kwargs):
		return super(IncidenciaList, self).dispatch(*args, **kwargs)


	# PARA UN LISTVIEW  PERSONALIZADO SEGUN SE ESCOJA
	# http://stackoverflow.com/questions/22902457/django-listview-customising-queryset		

class IncidenciaCreate(CreateView):
	model = Incidencia	
	template_name = 'incidencia/incidencia/incidencia_create_form.html'
	form_class = IncidenciaForm
	success_url = reverse_lazy('incidencia_list')

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.add_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):		
		return super(IncidenciaCreate, self).dispatch(*args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(IncidenciaCreate, self).get_form_kwargs()
		kwargs.update({'my_user': self.request.user})
		return kwargs

	# def get_context_data(self, **kwargs):
	# 	context = super(IncidenciaCreate, self).get_context_data(**kwargs)
	# 	if self.request.POST:
	# 		context['formset'] = BienFormSet(self.request.POST)
	# 	else:
	# 		context['formset'] = BienFormSet()
	# 	return context

class IncidenciaUpdate(UpdateView):
	model = Incidencia	
	template_name = 'incidencia/incidencia/incidencia_create_form.html'
	form_class = IncidenciaForm
	success_url = reverse_lazy('incidencia_list')

	@method_decorator(login_required)
	@method_decorator(permission_required('incidencia.change_incidencia', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(IncidenciaUpdate, self).dispatch(*args, **kwargs)
	
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