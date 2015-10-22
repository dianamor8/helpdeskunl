# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.centro_asistencia.models import *
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils.dateparse import * 
from django.shortcuts import get_object_or_404



class form_agregar_centro_asistencia(ModelForm):	
	class Meta:
		model = Centro_Asistencia
		fields = 'nombre', 'descripcion', 'email', 'contacto',
		labels = {
			'nombre': ('Nombre:'),
			'descripcion': ('Actividad:'),			
			'email': ('Correo Electrónico:'),			
			'contacto': ('Contacto:'),			
		}
		error_messages = {
			'nombre': {'required': u"Este campo no puede estar vacío.",},
			'descripcion': {'required': u"Este campo no puede estar vacío.",},			
			'email': {'invalid': u"Ingrese un valor válido.",},			
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del centro de asistencia.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción del centro de asistencia.',}),				
			# 'administradores': forms.Select(attrs={'class':'form-control required'}),
			'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección de correo electrónico de contacto.',}),
			'contacto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Números de contacto.',}),
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
		fields = 'nombre', 'descripcion', 'email', 'contacto',
		labels = {
			'nombre': ('Nombre:'),
			'descripcion': ('Actividad:'),			
			'email': ('Correo Electrónico:'),			
			'contacto': ('Contacto:'),			
		}
		error_messages = {
			'nombre': {'required': u"Este campo no puede estar vacío.", },
			'descripcion': {'required': u"Este campo no puede estar vacío.",},
			'email': {'invalid': u"Ingrese un valor válido.",},			
			'NON_FIELD_ERRORS': {'duplicado': u'Ya existe un centro de asistencia con este nombre.',},			
		}		
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del centro de asistencia.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción del centro de asistencia.',}),				
			# 'administradores': forms.Select(attrs={'class':'form-control required'}),
			'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección de correo electrónico de contacto.',}),
			'contacto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Números de contacto.',}),
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
	def __init__(self, *args, **kwargs):
		super(ServicioForm, self).__init__(*args, **kwargs)
		self.fields['estadistica'].empty_label = ">>>SELECCIONE<<<"		

	class Meta:
		model = Servicio
		exclude = 'centro', 'estado','creado_por',
		labels = {
			'estadistica': ('Estadística:'),
			'nombre': ('Nombre:'),
			'descripcion': ('Descripción:'),
			't_minimo': ('Tiempo mínimo de solución:'),	
			't_normal': ('Tiempo normal de solución:'),	
			't_maximo': ('Tiempo maximo de solución:'),	
		}

		error_messages = {
			'estadistica': {'required': u"Seleccione al menos una opción.",},
			'nombre': {'required': u"Este campo no puede estar vacío.",},
			'descripcion': {'required': u"Este campo no puede estar vacío.",},
			't_minimo': {'required': u"Este campo no puede estar vacío.", 'invalid': u"Ingrese una duración con formato válida.",},
			't_normal': {'required': u"Este campo no puede estar vacío.", 'invalid': u"Ingrese una duración con formato válida.",},
			't_maximo': {'required': u"Este campo no puede estar vacío.", 'invalid': u"Ingrese una duración con formato válida.",},
		}
		widgets = {
			'estadistica': forms.Select(attrs={'class':'form-control required'}),
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del servicio.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control expandable', 'placeholder':'Descripción del servicio.',}),				
			't_minimo': forms.HiddenInput(attrs={'class':'form-control', 'id':'tmin',}),
			't_normal': forms.HiddenInput(attrs={'class':'form-control', 'id':'tnor',}),
			't_maximo': forms.HiddenInput(attrs={'class':'form-control', 'id':'tmax',}),
			# 't_normal': forms.TextInput(attrs={'class':'form-control duracion', 'placeholder':'Formato > DD HH:MM:SS > Ej. 2 30:25:00',}),
			# 't_maximo': forms.TextInput(attrs={'class':'form-control duracion', 'placeholder':'Formato > DD HH:MM:SS > Ej. 2 30:25:00',}),
			
		}
	

	# def clean(self):
	# 	cleaned_data = super(ServicioForm, self).clean()
	# 	try:
	# 		t_minimo = cleaned_data.get("t_minimo")
	# 		t_normal = cleaned_data.get("t_normal")
	# 		t_maximo = cleaned_data.get("t_maximo")
	# 		estadistica = cleaned_data.get("estadistica")

	# 		minimo = parse_duration(str(t_minimo))
	# 		maximo = parse_duration(str(t_maximo))
	# 		normal = parse_duration(str(t_normal))

	# 		minimo_estadistica = parse_duration(str(estadistica.minima_duracion))
	# 		maximo_estadistica = parse_duration(str(estadistica.maxima_duracion))

	# 		if  normal < minimo:
	# 			msg = "El tiempo normal debe ser mayor o igual que el tiempo mínimo."
	# 			self.add_error('t_normal', msg)

	# 		if  maximo < normal:
	# 			msg = "El tiempo máximo debe ser mayor o igual que el tiempo normal."
	# 			self.add_error('t_maximo', msg)

	# 		print maximo_estadistica
	# 		print maximo

	# 		if minimo_estadistica > minimo:
	# 			msg = "La estadística mínima para este servicio es %s." %(estadistica.minima_duracion)
	# 			self.add_error('t_minimo', msg)

	# 		if  maximo > maximo_estadistica :
	# 			msg = "La estadística máxima para este servicio es %s." %(estadistica.maxima_duracion)
	# 			self.add_error('t_maximo', msg)
					
	# 	except Exception, e:
	# 		print e
	# 		return cleaned_data



	

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