from django.conf.urls import patterns, url
from django.views.defaults import page_not_found
from helpdeskunl.apps.accion.views import * 

urlpatterns = patterns('helpdeskunl.apps.accion',	
	#url(r'^incidencia/add$', IncidenciaCreate.as_view(), name='incidencia_add'),	
	url(r'^acciones/(?P<incidencia_id>\d+)/list$', AccionList.as_view(), name='accion_list'),
	url(r'^accion/(?P<incidencia_id>\d+)/add$', AccionCreate.as_view(), name='accion_add'),
	url(r'^accion/edit/(?P<pk>\d+)/$', AccionUpdate.as_view(), name='accion_update'),
	url(r'^accion/(?P<pk>\d+)/delete/$', AccionDelete.as_view(), name='accion_delete'),
	url(r'^diagnostico/(?P<incidencia_id>\d+)/add$', Diagnostico_Inicial_Create.as_view(), name='diagnostico_inicial'),
	url(r'^diagnostico/(?P<pk>\d+)/update$', Diagnostico_Inicial_Update.as_view(), name='diagnostico_inicial_update'),
	url(r'^solicitudes/(?P<accion_id>\d+)/(?P<incidencia_id>\d+)/$', SolicitudesList.as_view(), name='solicitudes_list'),
	url(r'^solicitud/(?P<accion_id>\d+)/add$', SolicitudCreate.as_view(), name='solicitud_add'),
	url(r'^solicitud/edit/(?P<pk>\d+)/$', SolicitudUpdate.as_view(), name='solicitud_update'),
)