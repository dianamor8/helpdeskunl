# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.problema.models import *
from helpdeskunl.apps.cambio.models import *
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.accion.models import *
from django.forms.models import inlineformset_factory
from helpdeskunl.apps.home.my_wiget import MultiSelectWidget 
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode, force_text
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy

class Diagnostico_InicialForm(forms.ModelForm):	
	class Meta:
		model = Diagnostico_Inicial
		fields = ('diagnostico',)
		labels = {			
			'diagnostico': ('Diagnostico:'),			
		}
		error_messages = {			
			'diagnostico': {'required': u"Este campo no puede estar vacío",},
		}
		widgets = {
			'diagnostico': forms.Textarea(attrs={'class':'form-control expandable' ,'placeholder':'Diagnostico inicial de la incidencia.',}),
		}

class AccionForm(forms.ModelForm):	
	class Meta:
		model = Accion
		fields = ('titulo', 'descripcion','visible_usuario',)
		labels = {			
			'titulo': ('Título:'),			
			'descripcion': ('Descripcion:'),
			'visible_usuario': ('Visible al solicitante:'),			
		}
		error_messages = {			
			'titulo': {'required': u"Este campo no puede estar vacío",},
			'descripcion': {'required': u"Este campo no puede estar vacío",},
		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título de la acción.',}),			
			'descripcion': forms.Textarea(attrs={'class':'form-control expandable' ,'placeholder':'Describa la acción realizada.',}),
			'visible_usuario': forms.CheckboxInput(attrs={'class':''}),			
		}


class Solicitud_RecursoForm(forms.ModelForm):	
	class Meta:
		model = Solicitud_Recurso
		fields = ('proveedor','recurso', 'tipo',)
		labels = {			
			'proveedor': ('Proveedor:'),			
			'recurso': ('Recurso:'),			
			'tipo': ('Tipo:'),
			# 'visible_usuario': ('Visible al solicitante:'),			
		}
		error_messages = {
			'proveedor': {'required': u"Seleccione una opción.",},
			'recurso': {'required': u"Este campo no puede estar vacío.",},
			'tipo': {'required': u"Seleccione una opción.",},
		}
		widgets = {
			'proveedor': forms.Select(attrs={'class':'form-control required'}),
			'recurso': forms.Textarea(attrs={'class':'form-control expandable' ,'placeholder':'Describa el recurso que desea solicitar.',}),
			'tipo': forms.Select(attrs={'class':'form-control required'}),
			# 'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título de la acción.',}),						
			# 'visible_usuario': forms.CheckboxInput(attrs={'class':''}),			
		}

