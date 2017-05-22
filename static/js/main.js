

/*
var t = document.getElementsByClassName('pub');

var posts_pub = document.getElementsByClassName('pub');
var pub_post = function(){
    var posted = posts_pub.getAttribute('value');
    $.post('/publicate_post', {
            pub_post: posted
    }, function(data){
        if(data === 1){
            swal('posted!');
            //window.location.replace("/main");
        }
        else if(data === 2){
            swal('no publicate');
        }
        else if(data === 3){
            //swal('Oops...', 'bad login');
        }
    });
};
posts_pub.addEventListener('click', pub_post);
*/
/**
function publicate_post(id){
    console.log(id);
    var post = document.getElementById(id + '_pub');
    var posted = post.getAttribute('value');
    console.log(posted);
    $.post('/publicate_post', {
            pub: posted
    }, function(data){
        if(data === 1){
            swal('posted!');
            //window.location.replace("/main");
        }
        else if(data === 2){
            swal('no publicate');
        }
        else if(data === 3){
            //swal('Oops...', 'bad login');
        }
    });
}*/
/**$(function() {
  $('#log-out').bind('click', function() {
    $.post('/logout', {
    }, function(data) {
      // $("#log-out").hide();
      // $("#sign").removeClass('hidden');
        window.location.reload();
    });
  });
});*/

var _submit = document.getElementById('_submit'),
_file = document.getElementById('_file'),
_progress = document.getElementById('_progress');
var upload = function(){
    if(_file.files.length === 0){
        return;
    }
    var data = new FormData();
    data.append('SelectedFile', _file.files[0]);

    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if(request.readyState == 4){
            try {
                var resp = JSON.parse(request.response);
            } catch (e){
                var resp = {
                    status: 'error',
                    data: 'Unknown error occurred: [' + request.responseText + ']'
                };
            }
            console.log(resp.status + ': ' + resp.data);
            swal('loaded');
            _progress.style.width = 0 + '%';
        }
    };

    request.upload.addEventListener('progress', function(e){
        _progress.style.width = Math.ceil(e.loaded/e.total) * 100 + '%';
    }, false);

    request.open('POST', '/upload');
    request.send(data);
};
_submit.addEventListener('click', upload);




(function() {
  
  'use strict';

  $('.input-file').each(function() {
    var $input = $(this),
        $label = $input.next('.js-labelFile'),
        labelVal = $label.html();
    
   $input.on('change', function(element) {
      var fileName = '';
      if (element.target.value) fileName = element.target.value.split('\\').pop();
      fileName ? $label.addClass('has-file').find('.js-fileName').html(fileName) : $label.removeClass('has-file').html(labelVal);
   });
  });

})();
   