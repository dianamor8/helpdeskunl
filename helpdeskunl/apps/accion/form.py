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
from django.db.models import Q

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
	def __init__(self, *args, **kwargs):
		my_user = kwargs.pop('my_user')
		super(Solicitud_RecursoForm, self).__init__(*args, **kwargs)
		self.fields['proveedor']=forms.ModelChoiceField(empty_label='>> SELECCIONE <<', queryset=Contacto.objects.filter(Q(tipo='1')|Q(perfil=my_user)), widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['proveedor'].error_messages = {'required': 'Seleccione quien proveerá el recurso.'}
		self.fields['tipo'].empty_label = ">> SELECCIONE <<"		

	class Meta:
		model = Solicitud_Recurso
		fields = ('recurso', 'proveedor', 'tipo', 'esperar', 'notificar_email')
		widgets = {
			'proveedor': forms.Select(attrs={'class':'form-control required'}),
			'recurso': forms.Textarea(attrs={'class':'form-control' ,'placeholder':'Describa el recurso que desea solicitar.',}),
			'tipo': forms.Select(attrs={'class':'form-control required'}),	
			'esperar': forms.RadioSelect,
			'notificar_email': forms.RadioSelect,			
		}
		labels = {			
			'proveedor': ('Proveedor:'),			
			'recurso': ('Recurso:'),			
			'tipo': ('Tipo:'),
			'esperar': ('¿Dejar la incidencia en espera del recurso?:'),
			'notificar_email': ('Notificar por email:'),
			# 'visible_usuario': ('Visible al solicitante:'),			
		}
		error_messages = {
			'proveedor': {'required': u"Seleccione una opción.",},
			'recurso': {'required': u"Este campo no puede estar vacío.",},
			'tipo': {'required': u"Seleccione una opción.",},			
		}
		

