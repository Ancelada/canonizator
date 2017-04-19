import sys
import os
from bs4 import BeautifulSoup
import requests
import pymorphy2
import binascii

# path = os.path.dirname(sys.modules[__name__].__file__)
# path = os.path.join(path, '..')
# sys.path.insert(0, path)
# __path__ = os.path.dirname(os.path.abspath(__file__))


class Vikidict():

	def __init__(self):
		self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        }
		self.path = os.path.dirname(os.path.abspath(__file__))
		self.morth = pymorphy2.MorphAnalyzer()

	def __page_soup(self, url):
		page_content = self.__get_page_content(url)
		return BeautifulSoup(page_content, 'lxml')

	def __get_page_content(self, url):
		return requests.get(url, headers=self.headers).text

	def __get_synonim_list(self, page_soup):
		h4 = page_soup.find_all('h4')
		for tag in h4:
			if tag.span.string == 'Синонимы':
				h4 = tag
				break
		if len(h4) > 0:
			try:
				a_arr = h4.next_sibling.next_sibling.find_all('a')
				synonims = []
				for a in a_arr:
					if a.get('title') != None:
						print (a['title'])
						synonims.append(a['title'])
				return synonims
			except:
				return []
		else:
			return []

	def parse_to_morph(self, word):
		return self.morth.parse(word)[0]

	def normalize_word(self, parsed_to_morph):
		normal_form = parsed_to_morph.normal_form
		return normal_form

	def start(self, words):
		result = []
		for word in words:
			POS = self.parse_to_morph(word.name).tag.POS
			page_soup = self.__page_soup('https://ru.wiktionary.org/wiki/{0}'.format(word.name))
			synonims = self.__get_synonim_list(page_soup)
			synonims = self.__remove_different_pos(POS, synonims)
			result.append({
				'id': word.id,
				'word': word.name,
				'synonims': self.__convert_synonims(synonims)
			})
		return result

	def __convert_synonims(self, synonims):
		result = []
		for synonim in synonims:
			result.append({'synonim': synonim, 'crc32': self.__convert_crc32(synonim)})
		return result

	def __remove_different_pos(self, POS, synonims):
		for key, value in enumerate(synonims):
			value = self.parse_to_morph(value)
			synonims[key] = value.normal_form
			if value.tag.POS != POS:
				del synonims[key]
				return self.__remove_different_pos(POS, synonims)
		return synonims

	def __convert_crc32(self, value):
		value_bytes=bytes(value, 'utf-8')
		return binascii.crc32(value_bytes)