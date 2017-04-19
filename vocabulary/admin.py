from django.contrib import admin
from vocabulary.models import *
from django_mptt_admin.admin import DjangoMpttAdmin

class NOUNAdmin(DjangoMpttAdmin):
	pass
admin.site.register(NOUN, NOUNAdmin)