from django.contrib import admin

# Register your models here.
from helpdeskunl.apps.incidencia.models import *

# admin.site.register(Incidencia)
# admin.site.register(Dependencia)
# admin.site.register(Categoria_Equipo)
# admin.site.register(Marca_Equipo)
# admin.site.register(Equipo)
# admin.site.register(Codigo_Bodega)
# admin.site.register(Detalle_Equipos)
# admin.site.register(Bien)
# admin.site.register(Caracteristica_Bien)


class Caracteristica_BienInline(admin.TabularInline):
	model = Caracteristica_Bien
	extra = 1

class BienAdmin(admin.ModelAdmin):
	inlines = [Caracteristica_BienInline]

admin.site.register(Incidencia)
admin.site.register(Bien, BienAdmin)