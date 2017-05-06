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
		self.statuses_colors={
			None: 'remind',
			1: '#1b9e77',
			0: '#7570b3',
			-1: '#d95f02',
			-2: 'gold',
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
				grammem['table'].objects.filter(Tone__isnull=False).values('id'))

			grammem['with_tone_by_user'] = len(
				grammem['table'].objects.filter(Tone__isnull=False, User_id=user_id).values('id'))

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
		return chart_array

	def build_tone_statistics_common(self, grammems):
		chart_array = []
		for grammem in grammems:
			statistics = list(grammem['table'].objects.filter(Tone__isnull=False).values(
				'Tone',
			).annotate(Count('Tone')))

			chart_array_line = {
				'name': grammem['name'],
				'name_rus': grammem['name_rus'],
				'data': [],
				'id': 'common_{0}'.format(grammem['name']),
			}

			chart_array_line['data'].append(['tone', 'count', {'role': 'style'}])

			for key, value in self.statuses.items():
				if any(key == statistic['Tone'] for statistic in statistics):

					filtered = [statistic['Tone__count'] for statistic in statistics \
						 if statistic['Tone'] == key]

					count = 0

					for filtered_value in filtered:
						count+= filtered_value

					chart_array_line['data'].append([
						value,
						count,
						self.statuses_colors[key],
					])
			chart_array.append(chart_array_line)
		return chart_array

	def build_user_select_table(self, users, grammems):
		result = []
		for user in users:

			result_line = {'name': user.username, 'id': user.id, 'count': 0}

			for grammem in grammems:
				grammem_count = len(grammem['table'].objects.filter(
					Tone__isnull=False, User_id=user.id).values('id'))
				result_line['count']+=grammem_count

			result.append(result_line)
		return {'users': result}

	def build_user_grammems(self, user_id, grammems):
		result = []
		for grammem in grammems:
			grammem_count = len(grammem['table'].objects.filter(
				Tone__isnull=False, User_id=user_id
			).values('id'))
			result_line = {
				'name': grammem['name'],
				'name_rus': grammem['name_rus'],
				'count': grammem_count,
				'url': grammem['url'],
			}
			result.append(result_line)
		return {
			'grammems': result,
			'user_id': user_id,
		}

	def build_user_grammem(self, user_id, grammem, grammems, page):
		
		offset = int(page)*10

		grammem_table = [gr for gr in grammems if gr['url'] == grammem][0]['table']

		result = {}

		result['words'] = list(grammem_table.objects.filter(
			User_id=user_id,
			parent_id__isnull=True,
		).values('name', 'Tone', 'id')[offset:10+offset])

		result['user_id'] = user_id
		result['url'] = grammem
		result['name_rus'] = [gr for gr in grammems if gr['url'] == grammem][0]['name_rus']
		result['name'] = [gr for gr in grammems if gr['url'] == grammem][0]['name']
		result['page'] = int(page)

		max_page_no = int(
			len(grammem_table.objects.filter(User_id=user_id, parent_id__isnull=True).values('id'))/10)+1

		result['pages'] = []
		for page_no in range(0, max_page_no, 1):
			if page_no == int(page):
				result['pages'].append({'no': page_no, 'selected': 1})
			else:
				result['pages'].append({'no': page_no, 'selected': 0})

		return result