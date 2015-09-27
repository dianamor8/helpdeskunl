# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.accion.models import *
from helpdeskunl.apps.cambio.models import *
from helpdeskunl.apps.centro_asistencia.models import *
from helpdeskunl.apps.usuarios.models import *
from django.forms.models import inlineformset_factory
from helpdeskunl.apps.home.my_wiget import MultiSelectWidget 
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode, force_text
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy