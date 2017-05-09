import os
import sys
import re
import pymorphy2
import traceback
import psutil
import time
import binascii
from django.utils import timezone
from more_itertools import unique_everseen

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'canonizator'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'canonizator.settings'

from django.conf import settings
import django
django.setup()

from mainapp.models import *
from vocabulary.models import *
from mainapp.daemons.base import Base
from django.db.models import Max

class Emptys():

	def __init__(self):
		self.punctuations = re.compile('([-_<>?/\\".„”“%,{}@#!&()=+:;«»—$&£*])')
		self.replace_with_spaces = {
			'\n',
			'\r',
			'\r\n',
			'\v',
			'\x0b',
			'\f',
			'\x0c',
			'\x1c',
			'\x1d',
			'\x1e',
			'\x85',
			'\u2028',
			'\u2029',
			'<br>',
			'<br />'
			'<p>',
			'</p>',
			'...',
			'\t',
			'\xa0',
		}
		self.copypublication_fields = [
			'crawler_id',
			'name',
			'name_cyrillic',
			'title',
			'text',
			'author',
			'date',
			'id',
		]


		self.grammems_to_remove = {
			'NPRO',
			'PRED',
			'PREP',
			'CONJ',
			'PRCL',
			'INTJ',
			'ROMN',
			'UNKN'
		}

		self.grammems_to_remove_vocabulary = {
			'NPRO': [],
			'PRED': [],
			'PREP': [],
			'CONJ': [],
			'PRCL': [],
			'INTJ': [],
			'ROMN': [],
			'UNKN': [],			
		}

		self.grammems_to_remove_models = {
			'NPRO': NPRO,
			'PRED': PRED,
			'PREP': PREP,
			'CONJ': CONJ,
			'PRCL': PRCL,
			'INTJ': INTJ,
			'ROMN': ROMN,
			'UNKN': UNKN,
		}

		self.vocabulary = {
            'NOUN': [],
            'ADJF': [],
            'ADJS': [],
            'COMP': [],
            'VERB': [],
            'INFN': [],
            'PRTF': [],
            'PRTS': [],
            'GRND': [],
            'NUMR': [],
            'ADVB': [],
            'LATN': [],
            'NUMB': [],
            'intg': [],
            'real': [],
        }

		self.voc_models = {
        	'NOUN': NOUN,
            'ADJF': ADJF,
            'ADJS': ADJS,
            'COMP': COMP,
            'VERB': VERB,
            'INFN': INFN,
            'PRTF': PRTF,
            'PRTS': PRTS,
            'GRND': GRND,
            'NUMR': NUMR,
            'ADVB': ADVB,
            'LATN': LATN,
            'NUMB': NUMB,
            'intg': intg,
            'real': real,
        }

	def get_emptys(self):
		for key, vocabulary in self.voc_models.items():
			nbsp_lines = vocabulary.objects.filter(name__icontains=' ').values('id')
			print (len(nbsp_lines))

	def delete_emptys(self):
		for key, vocabulary in self.voc_models.items():
			nbsp_lines = vocabulary.objects.filter(name__icontains=' ').delete()

result = Emptys().get_emptys()