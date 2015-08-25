
from django.conf.urls import patterns, url
from helpdeskunl.apps.incidencia.views import * 

urlpatterns = patterns('helpdeskunl.apps.incidencia',	
	#APP INCIDENCIA->DEPENDENCIA
	# url(r'^add/dependencia/$', 'views.add_dependencia_view',name = 'view_add_dependencia'),
	# INCIDENCIA	
	url(r'^incidencia/add$', IncidenciaCreate.as_view(), name='incidencia_add'),
	url(r'^incidencia/list$', IncidenciaList.as_view(), name='incidencia_list'),
	url(r'^incidencia/edit/(?P<pk>\d+)/$', IncidenciaUpdate.as_view(), name='incidencia_update'),
	url(r'^incidencia/(?P<pk>\d+)/delete/$', IncidenciaDelete.as_view(), name='incidencia_delete'),
	url(r'^bien/add$', BienCreate.as_view(), name='bien_add'),

)