

// var _submit = document.getElementById('_submit'),
// _file = document.getElementById('_file'),
// _progress = document.getElementById('_progress');
// var upload = function(){
//     if(_file.files.length === 0){
//         return;
//     }
//     var data = new FormData();
//     data.append('SelectedFile', _file.files[0]);

//     var request = new XMLHttpRequest();
//     request.onreadystatechange = function(){
//         if(request.readyState == 4){
//             try {
//                 var resp = JSON.parse(request.response);
//             } catch (e){
//                 var resp = {
//                     status: 'error',
//                     data: 'Unknown error occurred: [' + request.responseText + ']'
//                 };
//             }
//             console.log(resp.status + ': ' + resp.data);
//             swal('loaded');
//             _progress.style.width = 0 + '%';
//         }
//     };

//     request.upload.addEventListener('progress', function(e){
//         _progress.style.width = Math.ceil(e.loaded/e.total) * 100 + '%';
//     }, false);

//     request.open('POST', '/upload');
//     request.send(data);
// };
// _submit.addEventListener('click', upload);




// (function() {
  
//   'use strict';

//   $('.input-file').each(function() {
//     var $input = $(this),
//         $label = $input.next('.js-labelFile'),
//         labelVal = $label.html();
    
//    $input.on('change', function(element) {
//       var fileName = '';
//       if (element.target.value) fileName = element.target.value.split('\\').pop();
//       fileName ? $label.addClass('has-file').find('.js-fileName').html(fileName) : $label.removeClass('has-file').html(labelVal);
//    });
//   });

// })();
   