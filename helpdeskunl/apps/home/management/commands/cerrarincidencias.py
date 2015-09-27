from django.core.management.base import BaseCommand, CommandError
from helpdeskunl.apps.incidencia.models import *
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

class Command(BaseCommand):
	help = 'Cierra incidencias caducadas'
	args = 'No requiere argumentos'

	# def add_arguments(self, parser):
	#     parser.add_argument('incidencia_id', nargs='+', type=int)

	def handle(self, *args, **options):
		# for incidencia_id in options['incidencia_id']:
		incidencias = Incidencia.objects.filter(estado_incidencia = '2', ~Q(caduca = None))
		for incidencia in incidencias:
			try:
				hoy = timezone.now()				
				if incidencia.caduca < hoy:
					incidencia.estado_incidencia = '3'
					incidencia.save()
					self.stdout.write('Incidencia cerrada automaticamente "%s"' % incidencia.titulo)
			except Incidencia.DoesNotExist:
				raise CommandError('Incidencia "%s" no existe' % incidencia.titulo)