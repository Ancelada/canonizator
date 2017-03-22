from django.db import models
from django.utils import timezone
from django_mysql.models import JSONField, Model

################
# копия публикаци из
class CopyPublication(Model):

	name = models.CharField(max_length=512, blank=True, null=True)
	title = models.CharField(max_length=1024, blank=True, null=True)
	text = models.TextField()
	date = models.DateTimeField(db_index=True)
	author = models.CharField(max_length=512, blank=True, null=True, db_index=True)

class CopyPublicationStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class CopyPublicationError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)
######################



##############################
# нормализованные публикации
class NormalizePublication(Model):

	title = models.CharField(max_length=512, blank=True, null=True)
	text = models.TextField()
	CopyPublication = models.ForeignKey(CopyPublication, on_delete=models.CASCADE, blank=True, null=True)

class NormalizePublicationStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class NormalizePublicationError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)

##################################