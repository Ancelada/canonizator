from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from django_mysql.models import Model
# Части речи в соответствии с OpenCorpora http://opencorpora.org/dict.php?act=gram


#имя существительное
class NOUN(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)



	def __str__(self):
		return self.name

#имя прилагательное(полное)
class ADJF(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

#имя прилагательное (краткое)
class ADJS(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

#компаратив
class COMP(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

#глагол (личная форма)
class VERB(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

#глагол (инфинитив)
class INFN(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

#причастие (полное)
class PRTF(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# причастие (краткое)
class PRTS(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# деепричастие
class GRND(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# числительное
class NUMR(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# наречие
class ADVB(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# латиница
class LATN(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# число 
class NUMB(Model):

	class MPTTMeta:
		order_insertion_by = ['crc32']
	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# целое число
class intg(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# вещественное число
class real(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

############################################################
### неосновные грамемы
############################################################


# местоимение
class NPRO(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# предикатив
class PRED(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# предлог
class PREP(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name	
		
# союз
class CONJ(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# частица
class PRCL(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# междометие
class INTJ(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name

# римское число
class ROMN(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name 


# не удалось разобрать
class UNKN(Model):

	name = models.CharField(max_length=512)
	crc32 = models.BigIntegerField(default=0, db_index=True)
	vikidict_scaned = models.BooleanField(default=False)
	vikidict_correction_tested = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
	date = models.DateTimeField(default=timezone.now)
	User = models.ForeignKey(User, blank=True, null=True)
	Tone = models.IntegerField(blank=True, null=True)
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name


#############################################################
# разбор синонимов
class VocabularyStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class VocabularyError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)

#############################################################
# проверка корректности слов
class IncorrectStatus(Model):

	status = models.CharField(max_length=256, blank=True, null=True)
	count = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)

class IncorrectError(Model):

	error = models.TextField()
	date = models.DateTimeField(default=timezone.now)