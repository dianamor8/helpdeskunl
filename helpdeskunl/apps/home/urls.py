# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.index_view, name='view_home'),
	url(r'^(?P<username>\w+)$', views.panel_view,name = 'view_panel'),	
)