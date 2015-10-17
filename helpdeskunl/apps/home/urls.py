# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views
from . import rest
from helpdeskunl.apps.home.views import * 
from helpdeskunl.apps.home.rest import * 

urlpatterns = patterns('',
	url(r'^$', views.index_view, name='view_home'),
	url(r'^(?P<username>\w+)$', views.panel_view,name = 'view_panel'),	
	url(r'^notificaciones/list$', NotificacionesList.as_view(), name='notificacion_list'),

	# AJAX
	url(r'^notificacion/ver/(?P<pk>\d+)$', 'helpdeskunl.apps.home.rest.notificacion_visto', name='notificacion_ver'),
)