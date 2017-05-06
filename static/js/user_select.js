$('.user_select').on('click', function(){
	user_id = parseInt($(this).attr('data-id'));
	window.location = '/vocabulary/user_grammems/'+user_id+'/';
});