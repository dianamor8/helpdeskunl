from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='tiene_grupo')
def tiene_grupo(user, group_name):
	try:
		group = Group.objects.get(name=group_name)
	except:
		return False  # group doesn't exist, so for sure the user isn't part of the group  
	return True if group in user.groups.all() else False