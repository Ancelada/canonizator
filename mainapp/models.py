import mptt
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from django.db import models
from django.utils import timezone
from django_mysql.models import JSONField, Model


################
# копия публикаци из
class CopyPublication(Model):
	crawler_id = models.BigIntegerField(blank=True, null=True, db_index=True)
	name = models.CharField(max_length=512, blank=True, null=True)
	name_cyrillic = models.CharField(max_length=512, blank=True, null=True)
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

	crawler_id = models.BigIntegerField(blank=True, null=True, db_index=True)
	name = models.CharField(max_length=512, blank=True, null=True)
	name_cyrillic = models.CharField(max_length=512, blank=True, null=True)
	title = models.CharField(max_length=512, blank=True, null=True)
	text = models.TextField()
	author = models.CharField(max_length=512, blank=True, null=True, db_index=True)
	pubdate = models.DateTimeField(db_index=True, null=True, blank=True)
	CopyPublication = models.ForeignKey(CopyPublication, on_delete=models.CASCADE, blank=True, null=True)
	title_words = JSONField()
	text_words = JSONField()
	title_hashes = JSONField()
	text_hashes = JSONField()
	date = models.DateTimeField(default=timezone.now)
	parent_id = models.BigIntegerField(blank=True, null=True, db_index=True)
	status = models.IntegerField(null=True, blank=True)

class NormalizePublicationStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class NormalizePublicationError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)

##################################

##################################
# хэши публикаций
class MakeHashesStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class MakeHashesError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)

#################################

#####################################
# поиск нечетких дублей
class PubCompareStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class PubCompareError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)