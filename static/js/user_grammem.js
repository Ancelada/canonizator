//изменение значения radiobox
$('.word_tone_change').on('click', function(){
	word_id = parseInt($(this).attr('data-id'));
	word_tone = parseInt($(this).attr('data-tone'));
	changeTone(word_id, word_tone);
});

function changeTone(word_id, word_tone){
	$.each(words_list, function(i){
		if (words_list[i]['id'] == word_id ){
			words_list[i]['Tone'] = word_tone;
			return false;
		}
	})
}

//сохранить набор слов
$('#user_grammem_save').on('click', function(){
	parameters = {};
	parameters['words'] = words_list;
	parameters['grammem_url'] = grammem_url;
	parameters['method'] = 'update_words';
	makeAjax(parameters);
});

function userGrammemReadAjax(data, parameters){
	location.reload();
}