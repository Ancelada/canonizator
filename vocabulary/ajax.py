from bulk_update.helper import bulk_update

from django.http import JsonResponse
from vocabulary.base import Base as VocabularyBase
from vocabulary.vocabulary import Voc
from .models import *


class VocAjax():
	def __init__(self):
		self.statuses = {
			'remind': None,
			'positive': 1,
			'neitral': 0,
			'negative': -1,
			'incorrect': -2,
		}

	def __get_list_of_words_ids(self, words):
		result = []

		for word in words:
			result.append(word['id'])

		return result

	def read_ajax(self, string, request):
		if string['method'] == 'submit_words':

			words = string['words']

			grammem_url = words[0]['grammem_url']

			grammem_table = Voc().get_table_by_grammem(
				grammem_url,
				VocabularyBase().grammems,
			)
			grammem_words = grammem_table.objects.filter(id__in=self.__get_list_of_words_ids(words))

			for grammem_word in grammem_words:
				for word in words:
					if grammem_word.id == word['id']:
						grammem_word.Tone = self.statuses[word['status']]
						grammem_word.User_id = request.user.id

			bulk_update(grammem_words)
			return JsonResponse({
				'grammem_url': grammem_url,
			})