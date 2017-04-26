var words = [];

//отправить слова
$('#submit_words').on('click', function(){
	parameters = {}
	parameters['method'] = 'submit_words';
	parameters['words'] = words;
	makeAjax(parameters);
});

//переход к разбору слов
$('.choose_grammem').on('click', function(){
	grammem = $(this).attr('data-id');
	window.location = '/vocabulary/grammems/'+grammem+'/';
});

//изменить значение radio
$('.word_radio').on('change', function(){
	word_id = parseInt($(this).attr('data-id'));
	status = $(this).val();
	addStatus(status, word_id)
});

function addStatus(status, word_id){
	$.each(words, function(i){
		if (words[i]['id'] == word_id){
			words[i]['status'] = status;
		}
	});
}

function readResponseGrammems(data, parameters){
	if (parameters['method'] == 'submit_words'){
		window.location = '/vocabulary/grammems/'+data['grammem_url']+'/';
	}
}

function Init(){
	$.each($('.word_line'), function(){
		words.push({'id': parseInt($(this).attr('data-id')), 'html': $(this), 'status': 'remind',
		'grammem_url': $(this).attr('data-url')});
	});
}

Init();