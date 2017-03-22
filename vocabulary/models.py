from django.db import models

# import binascii
# def convert_crc32():
# 	value_bytes=bytes(value, 'ascii')
# 	return binascii.crc32(value_bytes)

# Части речи в соответствии с OpenCorpora http://opencorpora.org/dict.php?act=gram


#имя существительное
class NOUN(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

#имя прилагательное(полное)
class ADJF(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

#имя прилагательное (краткое)
class ADJS(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

#компаратив
class COMP(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

#глагол (личная форма)
class VERB(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

#глагол (инфинитив)
class INFN(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

#причастие (полное)
class PRTF(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# причастие (краткое)
class PRTS(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# деепричастие
class GRND(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# числительное
class NUMR(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# наречие
class ADVB(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# латиница
class LATN(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# число 
class NUMB(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# целое число
class intg(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()

# вещественное число
class real(models.Model):
	name = models.CharField(max_length=512)
	name_int = models.BigIntegerField()