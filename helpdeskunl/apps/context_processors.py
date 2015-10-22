from helpdeskunl.apps.usuarios.models import *
from helpdeskunl.apps.home.models import *

def tipo_usuario(request):
	asesores = Perfil.asesores_tecnicos.all()
	jefes = Perfil.jefes_departamento.all()
	usuarios = Perfil.usuarios_finales.all()
	supers = Perfil.super_administradores.all()
	contador_notificaciones = Notificacion.objects.filter(estado=True, destinatario__id=request.user.id, visto=False).count()

	es_asesor = False
	es_jefe = False
	es_superadmin = False
	es_usuario_final = False

	mi_usuario = request.user
	
	if mi_usuario in asesores:
		es_asesor = True
	if mi_usuario in jefes:
		es_jefe = True
	if mi_usuario in usuarios:
		es_usuario_final = True
	if mi_usuario in supers:
		es_superadmin = True
		
	contexto = {'es_asesor':es_asesor,'es_jefe':es_jefe,'es_superadmin':es_superadmin,'es_usuario_final':es_usuario_final,'contador_notificaciones':contador_notificaciones,}
	return contexto

