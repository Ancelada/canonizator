from django.template.loader import render_to_string

class Voc():
	def __init__(self):
		pass

	def get_table_by_grammem(self, grammem_selected, grammems):
		for grammem in grammems:
			if grammem_selected==grammem['url']:
				return grammem['table']

	def build_table(self, grammems):
		for grammem in grammems:
			grammem['count'] = len(grammem['table'].objects.all().values('id'))

			grammem['with_tone'] = len(
				grammem['table'].objects.filter(Tone__isnull=False, parent_id__isnull=True).values('id'))
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