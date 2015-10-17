 # -*- coding: utf-8 -*-
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

# HELPDESK
from helpdeskunl.apps.incidencia.models import *
from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.home.models import *
from helpdeskunl.apps.centro_asistencia.templatetags.tags import *

from django.shortcuts import get_object_or_404
from django.utils import formats

@login_required
def notificacion_visto(request, pk):	
	notificacion = Notificacion.objects.get(id=int(pk))
	notificacion.visto = True
	notificacion.save()
	return HttpResponse(json, content_type='application/json')