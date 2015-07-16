from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', name='view_login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', name='view_logout'),
	url(r'^usuario/busqueda/$', 'helpdeskunl.apps.usuarios.rest.buscar_usuarios', name='view_buscar_usuarios'), 
)