# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe

class MultiSelectWidget(forms.SelectMultiple):
	class Media:
		css = {
			'all': (
				settings.MEDIA_URL + 'css/multi-select.css',
			)
		}
		js = (
			settings.MEDIA_URL + 'js/jquery.multi-select.js',
		)

	def __init__(self, language=None, attrs=None):
		self.language = language or settings.LANGUAGE_CODE[:2]
		super(MultiSelectWidget, self).__init__(attrs=attrs)

	def render(self, name, value, attrs=None):
		rendered = super(MultiSelectWidget, self).render(name, value, attrs)
		return rendered + mark_safe(u'''<script type="text/javascript">
			$(document).ready(function afterReady() {
				var elem = $('#id_%(name)s');
				elem.multiselect();
			});
			</script>''' % {'name':name})