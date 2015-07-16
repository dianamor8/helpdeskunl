# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.centro_asistencia.models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError


class form_agregar_centro_asistencia(ModelForm):	
	class Meta:
		model = Centro_Asistencia
		exclude = 'usuarios', 'estado'
		labels = {
			'nombre': ('Nombre:'),
			'descripcion': ('Descripción:'),			
		}
		error_messages = {
			'nombre': {'required': u"Este campo no puede estar vacío.",},
			'descripcion': {'required': u"Este campo no puede estar vacío.",},			
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del centro de asistencia.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción del centro de asistencia.',}),				
			# 'administradores': forms.Select(attrs={'class':'form-control required'}),
		}
	
	def clean_nombre(self):
		nombre = self.cleaned_data['nombre']
		centro_existente = Centro_Asistencia.objects.filter(nombre=nombre)
		if centro_existente:
			raise forms.ValidationError("Ya existe un centro de asistencia con ese nombre.")		
		return nombre
	

class Centro_Asistencia_UpdateForm(ModelForm):	
	class Meta:
		model = Centro_Asistencia
		exclude = 'usuarios', 'estado'
		labels = {
			'nombre': ('Nombre:'),
			'descripcion': ('Descripción:'),			
		}
		error_messages = {
			'nombre': {'required': u"Este campo no puede estar vacío.", },
			'descripcion': {'required': u"Este campo no puede estar vacío.",},
			'NON_FIELD_ERRORS': {'duplicado': u'Ya existe un centro de asistencia con este nombre.',},			
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del centro de asistencia.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción del centro de asistencia.',}),			
		}

	def registro_nombre_duplicado(self, id_centro):		
		nombre = self.cleaned_data['nombre']
		try:
			centro_existente = Centro_Asistencia.objects.get(nombre=nombre)
		except Centro_Asistencia.DoesNotExist:
			centro_existente = None
		
		if centro_existente:
			if centro_existente.id != id_centro:
				raise forms.ValidationError((self.Meta.error_messages['NON_FIELD_ERRORS'])['duplicado'],code='NON_FIELD_ERRORS',)	
	
	
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
	

###########
#TAL VEZ CODIGO UTIL
###########

# def clean_nombre(self):

	# 	nombre = self.cleaned_data['nombre']
	# 	print self.cleaned_data
		
	# 	centro_id = self.id
	# 	centro_existente = Centro_Asistencia.objects.filter(nombre=nombre)

	# 	if not centro_id:
	# 		if centro_existente:
	# 			raise forms.ValidationError("Ya existe un centro de asistencia con ese nombre")
	# 	else:
	# 		if centro_existente.id == centro_id:
	# 			return data
	# 		else:
	# 			raise forms.ValidationError("Ya existe un centro de asistencia con ese nombre")

#  raise forms.ValidationError(self.error_messages['duplicate_email'])


	# def __init__(self, *args, **kwargs):
	# 	super(ServicioForm, self).__init__(*args, **kwargs)
	# 		self.fields.keyOrder = ['nombre','descripcion','centro',]