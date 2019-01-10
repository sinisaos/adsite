from __future__ import unicode_literals
from django.contrib import admin
from .models import Ad, Attachment, Rent

admin.site.register(Ad)
admin.site.register(Attachment)
admin.site.register(Rent)
