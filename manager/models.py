from django.db import models
from django.utils import timezone


# Create your models here.

class Crawler(models.Model):
	
	name = models.CharField(max_length=512, blank=True, null=True)
	file_name = models.CharField(max_length=512, blank=True, null=True)
	imported = models.DateTimeField(default=timezone.now)

class Publication(models.Model):

	title = models.CharField(max_length=512, blank=True, null=True)
	text = models.TextField()
	date = models.DateTimeField(db_index=True)
	author = models.CharField(max_length=512, blank=True, null=True)
	url = models.URLField()
	crawler = models.ForeignKey(Crawler, on_delete=models.CASCADE, null=True)

class CanonizatorError(models.Model):
	module = models.CharField(max_length=512, blank=True, null=True)
	error = models.TextField()
	date = models.DateTimeField(db_index=True)