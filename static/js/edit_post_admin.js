/**
 * Created by MOISEEV on 12.04.2017.
 */
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
document.getElementById('save-changes-post').addEventListener('click',function () {
    var container = document.getElementById('save-changes-post');

    var id = container.getAttribute('value');

    tinyMCE.triggerSave();
    var text = tinyMCE.get('post_text').getContent();

    var title = $('#title').val();

    var select_element = document.getElementById("select-theme");
    selected_values = getSelectValues(select_element);
    selected_values = selected_values.toString();
	console.log(selected_values);

    $.post('/apply_changes', {
        id: id,
        title: title,
        text: text,
        tags: selected_values
    }, function(data){
        if(data === 1){
            swal('saved');
			//window.location.replace('/admin/posts');
        }
        else if(data === 2){
            swal('wtf');
        }
    });
     
});