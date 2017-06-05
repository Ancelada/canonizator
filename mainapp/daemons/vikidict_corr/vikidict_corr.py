import sys
import os
from bs4 import BeautifulSoup
import requests
import binascii

# path = os.path.dirname(sys.modules[__name__].__file__)
# path = os.path.join(path, '..')
# sys.path.insert(0, path)
# __path__ = os.path.dirname(os.path.abspath(__file__))


class VikidictCorr():

	def __init__(self):
		self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
        }
		self.path = os.path.dirname(os.path.abspath(__file__))
		self.statuses = {
			None: 'remind',
			1: 'positive',
			0: 'neitral',
			-1: 'negative',
			-2: 'incorrect',
		}

	def __page_soup(self, url):
		page_content = self.__get_page_content(url)
		return BeautifulSoup(page_content, 'lxml')

	def __get_page_content(self, url):
		return requests.get(url, headers=self.headers).text

	def __get_incorrect(self, page_soup):
		h1 = page_soup.find_all('h1')

		div = page_soup.find_all('div', class_='noarticletext')

		result = True

		for tag in h1:
			if tag.string != None:
				if 'Недопустимое название' in tag.string:
					result = False

		if len(div) > 0:
			result = False

		return result

	def start(self, words):
		result = []
		for word in words:
			page_soup = self.__page_soup('https://ru.wiktionary.org/wiki/{0}'.format(word.name))
			check_word = self.__get_incorrect(page_soup)
			if check_word == False:
				result.append({
					'id': word.id,
					'result': -2,
				})
			else:
				result.append({
					'id': word.id,
					'result': word.Tone,	
				})
		return result