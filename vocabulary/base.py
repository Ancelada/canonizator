from .models import *

class Base():
	def __init__(self):
		self.grammems = [
			{
				'name': 'NOUN',
				'url': 'noun',
				'table': NOUN,
				'name_rus': 'имя существительное',
			},
			{
				'name': 'ADJF',
				'url': 'adjf',
				'table': ADJF,
				'name_rus': 'имя прилагательное(полное)'
			},
			{
				'name': 'ADJS',
				'url': 'adjs',
				'table': ADJS,
				'name_rus': 'имя прилагательное (краткое)',
			},
			{
				'name': 'COMP',
				'url': 'comp',
				'table': COMP,
				'name_rus': 'компаратив',
			},
			{
				'name': 'VERB',
				'url': 'verb',
				'table': VERB,
				'name_rus': 'глагол (личная форма)',
			},
			{
				'name': 'INFN',
				'url': 'infn',
				'table': INFN,
				'name_rus': 'глагол (инфинитив)',
			},
			{
				'name': 'PRTF',
				'url': 'prtf',
				'table': PRTF,
				'name_rus': 'причастие (полное)',
			},
			{
				'name': 'PRTS',
				'url': 'prts',
				'table': PRTS,
				'name_rus': 'причастие (краткое)',
			},
			{
				'name': 'GRND',
				'url': 'grnd',
				'table': GRND,
				'name_rus': 'деепричастие',
			},
			{
				'name': 'NUMR',
				'url': 'numr',
				'table': NUMR,
				'name_rus': 'числительное',
			},
			{
				'name': 'ADVB',
				'url': 'advb',
				'table': ADVB,
				'name_rus': 'наречие',
			},
			{
				'name': 'LATN',
				'url': 'latn',
				'table': LATN,
				'name_rus': 'латиница',
			},
			{
				'name': 'NUMB',
				'url': 'numb',
				'table': NUMB,
				'name_rus': 'число',
			},
			{
				'name': 'intg',
				'url': 'intg',
				'table': intg,
				'name_rus': 'целое число',
			},
			{
				'name': 'real',
				'url': 'real',
				'table': real,
				'name_rus': 'вещественное число',
			},
			{
				'name': 'NPRO',
				'url': 'npro',
				'table': NPRO,
				'name_rus': 'местоимение',
			},
			{
				'name': 'PRED',
				'url': 'pred',
				'table': PRED,
				'name_rus': 'предикатив',
			},
			{
				'name': 'PREP',
				'url': 'prep',
				'table': PREP,
				'name_rus': 'предлог',
			},
			{
				'name': 'CONJ',
				'url': 'conj',
				'table': CONJ,
				'name_rus': 'союз',
			},
			{
				'name': 'PRCL',
				'url': 'prcl',
				'table': PRCL,
				'name_rus': 'частица',
			},
			{
				'name': 'INTJ',
				'url': 'intj',
				'table': INTJ,
				'name_rus': 'междометие',
			},
			{
				'name': 'ROMN',
				'url': 'romn',
				'table': ROMN,
				'name_rus': 'римское число',
			},
			{
				'name': 'UNKN',
				'url': 'unkn',
				'table': UNKN,
				'name_rus': 'не удалось разобрать',
			}
		]