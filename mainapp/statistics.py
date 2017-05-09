import datetime
import pytz
import locale
from itertools import groupby


from django.utils import timezone
from django.conf import settings
from django.db.models import Count


from .models import *
from vocabulary.models import *
from manager.models import Publication

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

class Statistics:

	
	def __init__(self):
		self.programs = [
			{
				'name': 'Скопированные публикации',
				'id': 'copy_publication',
				'tables': [
					{'name': 'Publication', 'table': CopyPublication},
					{'name': 'Status', 'table': CopyPublicationStatus},
					{'name': 'Error', 'table': CopyPublicationError},
				]
			}, 

			{
				'name': 'Нормализованные публикации',
				'id': 'normalize_publication',
				'tables': [
					{'name': 'Publication', 'table': NormalizePublication},
					{'name': 'Status', 'table': NormalizePublicationStatus},
					{'name': 'Error', 'table': NormalizePublicationError},
				]
			},
			{
				'name': 'Созданные хэши публикаций',
				'id': 'make_hash',
				'tables': [
					{'name': 'Publication', 'table': NormalizePublication},
					{'name': 'Status', 'table': MakeHashesStatus},
					{'name': 'Error', 'table': MakeHashesError},
				]
			}
		]

		self.poses = [
			{
				'name': 'NOUN',
				'name_rus': 'имя существительное',
				'table': NOUN,
			},
			{
				'name': 'ADJF',
				'name_rus': 'имя прилагательное (полное)',
				'table': ADJF,
			},
			{
				'name': 'ADJS',
				'name_rus': 'имя прилагательное (краткое)',
				'table': ADJS,
			},
			{
				'name': 'COMP',
				'name_rus': 'компаратив',
				'table': COMP,
			},
			{
				'name': 'VERB',
				'name_rus': 'глагол (личная форма)',
				'table': VERB,
			},
			{
				'name': 'INFN',
				'name_rus': 'глагол (инфинитив)',
				'table': INFN,
			},
			{
				'name': 'PRTF',
				'name_rus': 'причастие (полное)',
				'table': PRTF,
			},
			{
				'name': 'PRTS',
				'name_rus': 'причастие (краткое)',
				'table': PRTS,
			},
			{
				'name': 'GRND',
				'name_rus': 'деепричастие',
				'table': GRND,
			},
			{
				'name': 'NUMR',
				'name_rus': 'числительное',
				'table': NUMR,
			},
			{
				'name': 'ADVB',
				'name_rus': 'наречие',
				'table': ADVB,
			},
			{
				'name': 'LATN',
				'name_rus': 'латиница',
				'table': LATN,
			},
			{
				'name': 'NUMB',
				'name_rus': 'число',
				'table': NUMB,
			},
			{
				'name': 'intg',
				'name_rus': 'целое число',
				'table': intg,
			},
			{
				'name': 'real',
				'name_rus': 'вещественное число',
				'table': real,
			},
		]

		self.last_days = [
			timezone.now()-datetime.timedelta(days=6),
			timezone.now()-datetime.timedelta(days=5),
			timezone.now()-datetime.timedelta(days=4),
			timezone.now()-datetime.timedelta(days=3),
			timezone.now()-datetime.timedelta(days=2),
			timezone.now()-datetime.timedelta(days=1),
			timezone.now(),
		]

		self.statuses = {
			1: 'Уникальных',
			2: 'Перепечаток',
			3: 'Скопированных',
		}

	def __get_group_statistic_by_date(self, start_date, program_id):

		for program in self.programs:
			if program_id == program['id']:

				result = {'name': program['name'], 'columns': [], 'id': program['id']}

				for table in program['tables']:

					table_lines = table['table'].objects.filter(date__gte=start_date)

					for key, values in groupby(table_lines, key=lambda table_line: table_line.date.date()):
						if not (any(line['date'] == key for line in result['columns'])):
							result['columns'].append({
								'date': key,
								'Publication': [],
								'Status': [],
								'Error': [],
							})

					for table_line in table_lines:
						for line in result['columns']:
							if line['date'] == table_line.date.date():
								line[table['name']].append(table_line)

					for line in result['columns']:
						line[table['name']] = len(line[table['name']])

				return result

	def build_copy_and_normalize_publications_statistics(self, program_id):

		start_date  = (timezone.now()-datetime.timedelta(days=14))

		start_date = start_date.replace(hour = 0, minute = 0, second = 0)

		program = self.__get_group_statistic_by_date(start_date, program_id)

		program['chart_array'] = [
			['Дата', 'Публикаций', 'Успешных запросов', 'Ошибок']
		]
		for column in program['columns']:
			program['chart_array'].append([
				column['date'].strftime('%d-%m-%Y'),
				column['Publication'],
				column['Status'],
				column['Error'],
			])
		del program['columns']

		for chart_line in program['chart_array']:
			for key, value in enumerate(chart_line):
				if isinstance(value, list):
					chart_line[key] = 0
		return program

	def __get_synonim_words_count(self, less_day_words):
		count = 0
		for word in less_day_words:
			if word['level'] == 1 and word['vikidict_scaned'] == 1:
				count+=1
		return count

	def __get_unique_words_count(self, less_day_words):
		count = 0
		for word in less_day_words:
			if word['level'] == 0 and word['vikidict_scaned'] == 1:
				count+=1
		return count

	def __get_vikidict_scaned_words_count(self, less_day_words):
		count = 0
		for word in less_day_words:
			if word['vikidict_scaned']:
				count+=1
		return count

	def __get_voc_statistic_by_date(self, start_date):

		result = []

		for pos in self.poses:

			result_line = {
				'name': pos['name'],
				'name_rus': pos['name_rus'],
				'days': [],
			}

			for day in self.last_days:

				day_line  = {'day': day}

				less_day_words = pos['table'].objects.filter(date__lte=day).values(
					'id', 'vikidict_scaned', 'level')

				day_line['all_words'] = less_day_words.count()
				day_line['vikidict_scaned_words'] = self.__get_vikidict_scaned_words_count(less_day_words)
				day_line['unique_words'] = self.__get_unique_words_count(less_day_words)
				day_line['synonim_words'] = self.__get_synonim_words_count(less_day_words)

				result_line['days'].append(day_line)
			result.append(result_line)

		return result
		

	def __convert_to_google_chart(self, vocabularys_statistics):

		for statistics_line in vocabularys_statistics:

			google_chart = []
			google_chart.append(['Дата', 'Слов', 'Сканированных', 'Уникальных', 'Синонимов'])
			
			for day in statistics_line['days']:
				google_chart.append([
					day['day'].strftime('%d-%m-%Y'),
					day['all_words'],
					day['vikidict_scaned_words'],
					day['unique_words'],
					day['synonim_words'],
				])

			statistics_line['google_chart'] = google_chart

			del statistics_line['days']

		return vocabularys_statistics

	def build_vocabulary_statistics(self):

		start_date  = (timezone.now()-datetime.timedelta(days=14))

		start_date = start_date.replace(hour = 0, minute = 0, second = 0)

		vocabulary_statistics = self.__get_voc_statistic_by_date(start_date)

		vocabulary_statistics = self.__convert_to_google_chart(vocabulary_statistics)

		return vocabulary_statistics

	def build_common_statistics(self):

		statistics = []

		# статистика всего публикаций в менеджере, к скопироанному канонизатором
		manager_publications_count = Publication.objects.using(	'manager').all().values(
			'id').count()

		copy_publication_count = CopyPublication.objects.all().values(
			'id').count()

		normalize_publication_count = NormalizePublication.objects.all().values('id').count()

		with_hash_count = NormalizePublication.objects.exclude(title_hashes={}).values('id').count()

		with_status_count = NormalizePublication.objects.exclude(
			status__isnull=True).values('id').count()

		name = 'Общая статистика'

		chart_array = []
		chart_array.append(['Показатель', 'Значение'])
		chart_array.append(['Crawler', manager_publications_count])
		chart_array.append(['Скопированных', copy_publication_count])
		chart_array.append(['Нормализованных', normalize_publication_count])
		chart_array.append(['Хэшированных', with_hash_count])
		chart_array.append(['Фильтр нечетких дублей', with_status_count])


		statistics.append({'name':name, 'chart_array': chart_array, 'id': 'crawler_copys'})

		return statistics

	def build_statistics_pubcompare(self):

		statuses = NormalizePublication.objects.exclude(
			status__isnull=True).values('status').annotate(Count('status'))

		chart_array = []
		chart_array.append(['статус', 'количество публикаций'])

		for status in statuses:
			chart_array.append([self.statuses[status['status']], status['status__count']])

		name = 'Разобранные статусы, количество'

		return {
			'name': name,
			'chart_array': chart_array,
			'id': 'statuses',
		}