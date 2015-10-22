from django.conf.urls import patterns, url
from helpdeskunl.apps.centro_asistencia.views import * 

urlpatterns = patterns('helpdeskunl.apps.centro_asistencia',	
	# VIEW
	url(r'^lista/centro_asistencia/$', 'views.lista_centro_asistencia',name = 'view_lista_centro_asistencia'),	

	# LIST, DETAIL, CREATE, CHANGE, DELETE VIEWS
		# CENTRO DE ASISTENCIAw
	url(r'^centro_asistencia/(?P<pk>[-\d]+)/$', Centro_Asistencia_DetailView.as_view(), name='view_centro_asistencia_detail'),
	url(r'^listageneral/centro_asistencia/$', Centro_Asistencia_General.as_view(), name='centro_asistencia_list'),	
	url(r'^centro_asistencia/edit/(?P<pk>\d+)/$', Centro_AsistenciaUpdate.as_view(), name='centro_asistencia_update'),
	url(r'^centro_asistencia/add$', Centro_AsistenciaCreate.as_view(), name='centro_asistencia_add'),
	url(r'^centro_asistencia/(?P<pk>\d+)/delete/$', Centro_AsistenciaDelete.as_view(), name='centro_asistencia_delete'),
		#SERVICIOS CENTRO DE ASISTENCIA 
	url(r'^servicio/add/(?P<centro>\d+)$', ServicioCreate.as_view(), name='servicio_add'),
	url(r'^servicio/(?P<pk>\d+)/$', ServicioUpdate.as_view(), name='servicio_update'),
	url(r'^servicio/(?P<pk>\d+)/delete/$', ServicioDelete.as_view(), name='servicio_delete'),
	# REST
	# url(r'^centro_asistencia/add$', 'rest.centro_asistencia_add_ajax',name = 'view_centro_asistencia_add'),			
	url(r'^centro_asistencia/add_usuario$', 'rest.agregar_usuario',name = 'view_agregar_usuario_centro_asistencia'),
	url(r'^centro_asistencia/remove_usuario$', 'rest.eliminar_usuario',name = 'view_eliminar_usuario_centro_asistencia'),
	url(r'^rest/centro_asistencia/verificar_duracion$', 'rest.verificar_duracion',name = 'view_verificar_duracion_centro_asistencia'),
	url(r'^rest/centro_asistencia/verificar_estadistica$', 'rest.verificar_estadistica',name = 'view_verificar_estadistica_centro_asistencia'),
	url(r'^rest/get_notificaciones$', 'rest.get_notificaciones',name = 'view_get_notificaciones_centro_asistencia'),
	
)