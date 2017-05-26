function getSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;

  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];

    if (opt.selected) {
      result.push(opt.value || opt.text);
    }
  }
  return result;
}
window.onload = $('#post_text').val('');
$(function() {
  $('.save-post-button').bind('click', function(){
	  tinyMCE.triggerSave();
	  var text = tinyMCE.get('post_text').getContent();
	  var title = $('#title').val();
	  var select_element = document.getElementById("select-theme");
	  selected_values = getSelectValues(select_element);
	  selected_values = selected_values.toString();
		console.log(text,title,selected_values);
		if(title== "" || text== "" || selected_values == ""){
			swal('заполните пустые поля');
		}
		else{
			$.post('/add', {
			title: title,
			text: text,
			tags: selected_values
			}, function(data){
				if(data == true)
				swal('post created');
				else
				swal('Oops...');
			});
		}
	
  });
});

