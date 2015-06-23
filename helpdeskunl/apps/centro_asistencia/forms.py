# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.centro_asistencia.models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple


class form_agregar_centro_asistencia(ModelForm):	
	# administradores = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(groups__name='Jefe Departamento'), label='Usuarios Administradores:', help_text='Seleccione los usuarios administradores del centro de asistencia.', widget=FilteredSelectMultiple('Usuarios', False, attrs={'rows': '10',}))
	# tecnicos = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(groups__name='Técnico Operativo'), label='Asesores Técnicos:',help_text='Seleccione los asesores técnicos del centro de asistencia.', widget=FilteredSelectMultiple('Asesores Técnicos', False, attrs={'rows': '10',}))	
	class Meta:
		model = Centro_Asistencia
		exclude = 'usuarios',
		labels = {
			'nombre': ('Nombre:'),
			'descripcion': ('Descripción:'),			
		}
		error_messages = {
			'nombre': {'required': u"Este campo no puede estar vacío.",},
			'descripcion': {'required': u"Este campo no puede estar vacío.",},			
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Del Centro De Asistencia.',}),			
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripción Del Centro De Asistencia.',}),				
			# 'administradores': forms.Select(attrs={'class':'form-control required'}),
		}

		# http://blog.jayapal.in/2009/08/reuse-django-admin-filteredselectmultip.html
		# https://groups.google.com/forum/#!topic/django-users/xxUlZgICDBE
		# <script type="text/javascript">window.__admin_media_prefix__ = "/static/admin/";</script>
		# <script type="text/javascript" src="/my_url/jsi18n/"></script>
		# <script type="text/javascript" src="/static/admin/js/core.js"></script>
		# <script type="text/javascript" src="/static/admin/js/actions.js"></script>
		# <script type="text/javascript" src="/static/admin/js/SelectBox.js"></script>
		# <script type="text/javascript" src="/static/admin/js/SelectFilter2.js"></script> -->

class ServicioForm(ModelForm):
	class Meta:
		model = Servicio
		exclude = 'centro',
		labels = {
			'nombre': ('Nombre:'),
			'descripcion': ('Descripción:'),			
		}
		error_messages = {
			'nombre': {'required': u"Este campo no puede estar vacío.",},
			'descripcion': {'required': u"Este campo no puede estar vacío.",},			
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del servicio.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción del servicio.',}),	
		}
	
	# def __init__(self, *args, **kwargs):
	# 	super(ServicioForm, self).__init__(*args, **kwargs)
	# 		self.fields.keyOrder = ['nombre','descripcion','centro',]