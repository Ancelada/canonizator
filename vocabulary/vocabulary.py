from django.template.loader import render_to_string
from django.db.models import Count
from django.contrib.auth.models import User

class Voc():

	def __init__(self):
		self.statuses = {
			None: 'remind',
			1: 'positive',
			0: 'neitral',
			-1: 'negative',
			-2: 'incorrect',
		}
		self.diagram_columns = [
			'name',
			'positive',
			'neitral',
			'negative',
			'incorrect',
		]

	def get_table_by_grammem(self, grammem_selected, grammems):
		for grammem in grammems:
			if grammem_selected==grammem['url']:
				return grammem['table']

	def build_table(self, grammems, user_id):
		for grammem in grammems:
			grammem['count'] = len(grammem['table'].objects.all().values('id'))

			grammem['with_tone'] = len(
				grammem['table'].objects.filter(Tone__isnull=False, parent_id__isnull=True).values('id'))

			grammem['with_tone_by_user'] = len(
				grammem['table'].objects.filter(Tone__isnull=False).values('id'))

		return render_to_string('grammems.html', {
			'grammems': grammems,			
		})

	def build_grammem_page(self, grammem, grammems):

		table = self.get_table_by_grammem(grammem, grammems)

		words = table.objects.filter(Tone__isnull=True)[:10]

		return render_to_string('grammem.html', {
			'words': words,	
			'grammem': grammem,
		})

	def __add_usernames(self, query_dict):

		Users = User.objects.all().values('id', 'username')

		for line in query_dict:
			for user in  Users:
				if line['User_id'] == user['id']:
					line['name'] = user['username']

	def __add_tone_names(self, query_dict):
		for line in query_dict:
			if line['Tone'] in self.statuses:
				line['Tone'] = self.statuses[line['Tone']]

	def __add_tones_to_users(self, statistics):
		result = {}
		for statistic in statistics:
			print (statistic)
			if not statistic['name'] in result:
				result[statistic['name']] = []
				result[statistic['name']].append({
					'tone': 'name',
					'count': statistic['name'],	
				})
				result[statistic['name']].append({
					'tone': statistic['Tone'],
					'count': statistic['Tone__count']
				})
			else:
				if not any(statistic['Tone'] == res['tone'] for res in result[statistic['name']]):
					result[statistic['name']].append({
						'tone': statistic['Tone'],
						'count': statistic['Tone__count']	
					})
				else:
					count = [res for res in result[statistic['name']] if res['tone'] == statistic['Tone']][0]
					count['count'] += statistic['Tone__count']
		print ('------------------')
		return result

	def build_tone_statistics(self, grammems):

		chart_array = []

		for grammem in grammems:

			statistics = list(grammem['table'].objects.filter(Tone__isnull=False).values(
				'User_id',
				'Tone',
			).annotate(Count('Tone')))

			self.__add_usernames(statistics)
			self.__add_tone_names(statistics)

			tones_dict = self.__add_tones_to_users(statistics)

			chart_array_line = {
				'name': grammem['name'],
				'name_rus': grammem['name_rus'],
				'data': [],
				'id': grammem['name']
			}

			chart_array_line['data'].append(self.diagram_columns)

			for key, tone_dict in tones_dict.items():
				subline = []
				for diagram_column in self.diagram_columns:
					doubled = 0
					for tone in tone_dict:
						if tone['tone'] == diagram_column:
							subline.append(tone['count'])
							doubled = 1
					if doubled == 0:
						subline.append(0)

				chart_array_line['data'].append(subline)

			chart_array.append(chart_array_line)
		print (chart_array)
		return chart_array