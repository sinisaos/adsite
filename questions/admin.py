from __future__ import unicode_literals

from django.contrib import admin

from .models import Answer, Question

admin.site.register(Question)
admin.site.register(Answer)
