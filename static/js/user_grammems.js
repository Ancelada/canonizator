$('.user_grammems').on('click', function(){
	user_id = parseInt($(this).attr('data-user'));
	grammem = $(this).attr('data-grammem');
	window.location = '/vocabulary/user_grammem/'+user_id+'/'+grammem+'/0/';
});