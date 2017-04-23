from django.utils import timezone
from django.db import models
import mptt
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from django_mysql.models import Model
# Части речи в соответствии с OpenCorpora http://opencorpora.org/dict.php?act=gram


#имя существительное
class NOUN(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

mptt.register(NOUN, order_insertion_by=['name'])

#имя прилагательное(полное)
class ADJF(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

#имя прилагательное (краткое)
class ADJS(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

#компаратив
class COMP(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

#глагол (личная форма)
class VERB(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

#глагол (инфинитив)
class INFN(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

#причастие (полное)
class PRTF(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# причастие (краткое)
class PRTS(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# деепричастие
class GRND(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# числительное
class NUMR(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# наречие
class ADVB(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# латиница
class LATN(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# число 
class NUMB(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# целое число
class intg(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# вещественное число
class real(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

############################################################
### неосновные грамемы
############################################################


# местоимение
class NPRO(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# предикатив
class PRED(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# предлог
class PREP(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name	
		
# союз
class CONJ(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# частица
class PRCL(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# междометие
class INTJ(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name

# римское число
class ROMN(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name 


# не удалось разобрать
class UNKN(MPTTModel):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	parent = TreeForeignKey('self', blank=True, null=True, \
	 related_name='children', db_index=True)
	date = models.DateTimeField(default=timezone.now)

	tree = TreeManager()

	def __str__(self):
		return self.name


#############################################################
class VocabularyStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class VocabularyError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)