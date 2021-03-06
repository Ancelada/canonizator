from bulk_update.helper import bulk_update

from django.http import JsonResponse
from vocabulary.base import Base as VocabularyBase
from vocabulary.vocabulary import Voc
from .models import *


class VocAjax():
	def __init__(self):
		pass

	def __get_list_of_words_ids(self, words):
		result = []

		for word in words:
			result.append(word['id'])

		return result

	def read_ajax(self, string, request):
		if string['method'] == 'update_words':

			words = string['words']

			grammem_url = string['grammem_url']

			grammem_table = Voc().get_table_by_grammem(
				grammem_url,
				VocabularyBase().grammems,
			)

			grammem_words = grammem_table.objects.filter(id__in=self.__get_list_of_words_ids(words))

			for grammem_word in grammem_words:
				if grammem_word.Tone == [
						word for word in words if word['id'] == grammem_word.id
					][0]['Tone']:
					grammem_words = grammem_words.exclude(id=grammem_word.id)

			synonims_of_grammem_words = grammem_table.objects.filter(
				parent_id__in=self.__get_list_of_words_ids(words))

			for grammem_word in grammem_words:
				for word in words:
					if grammem_word.id == word['id']:

						for synonim in synonims_of_grammem_words:
							if synonim.parent_id == word['id']:
								synonim.Tone = word['Tone']
								synonim.User_id = request.user.id

						grammem_word.Tone = word['Tone']
						grammem_word.User_id = request.user.id

			bulk_update(grammem_words)

			if synonims_of_grammem_words.exists():
				bulk_update(synonims_of_grammem_words)

			return JsonResponse({
				'answer': 'ok',
			})

		if string['method'] == 'submit_words':

			words = string['words']

			grammem_url = words[0]['grammem_url']

			grammem_table = Voc().get_table_by_grammem(
				grammem_url,
				VocabularyBase().grammems,
			)

			grammem_words = grammem_table.objects.filter(id__in=self.__get_list_of_words_ids(words))
			synonims_of_grammem_words = grammem_table.objects.filter(
				parent_id__in=self.__get_list_of_words_ids(words))

			for grammem_word in grammem_words:
				for word in words:
					if grammem_word.id == word['id']:

						for synonim in synonims_of_grammem_words:
							if synonim.parent_id == word['id']:
								synonim.Tone = word['status']
								synonim.User_id = request.user.id
						grammem_word.Tone = word['status']
						grammem_word.User_id = request.user.id

			bulk_update(grammem_words)

			if synonims_of_grammem_words.exists():
				bulk_update(synonims_of_grammem_words)

			return JsonResponse({
				'grammem_url': grammem_url,
			})