var emailRegular = /@/;
var russian = /[А-Яа-яЁё]/;
var spec = /[\s\\/*-?&()^%$#'";:!`,]/;
var spec_password = /[^0-9a-zA-ZА-Яа-яйЙёЁ]/;
var spec_login = /[^0-9a-zA-Z@._]/;
var login = document.getElementById("login");
var password = document.getElementById("password");
var errors = {  email_length: 0,
                email_dog: 0,
                email_rus: 0,
                email_symbols: 0,
                password_length: 0,
                password_rus: 0,
                password_symbols: 0  };

document.addEventListener("DOMContentLoaded",function (event) {
    login.value = "";
    password.value = "";
    
    var ul_email = document.getElementById('ul_email');
    var ul_pass = document.getElementById('ul_pass');

    login.addEventListener("input", function (e) {
        var length = $(login).val().length;
        if(length < 1)
            $(ul_email).hide(100);
        else
            $(ul_email).show(100);

        //#1 length
        if(length >= 8 && length < 50){
            $('li.l_len').css('color', 'green');
            errors['email_length'] = 0;}
        else{
            $('li.l_len').css('color', 'tomato');
            errors['email_length'] = 1;}

        //#2 use @
        if(emailRegular.test(login.value)){
            $('li.l_dog').css('color', 'green');
            errors['email_dog'] = 0;}
        else{
            $('li.l_dog').css('color', 'tomato');
            errors['email_dog'] = 1;}

        //#3 russian language
        if(russian.test(login.value)){
            $('li.l_rus').css('color', 'tomato');
            errors['email_rus'] = 1;}
        else{
            $('li.l_rus').css('color', 'green');
            errors['email_rus'] = 0;}

        //#4 spec symbols
        if(spec_login.test(login.value)){
            $('li.l_spec').css('color', 'tomato');
            errors['email_symbols'] = 1;}
        else{
            $('li.l_spec').css('color', 'green');
            errors['email_symbols'] = 0;}
    });

    password.addEventListener("input", function (e) {
        var length = $(password).val().length;
        if(length < 1)
            $(ul_pass).hide(100);
        else
            $(ul_pass).show(100);

        //#1 length
        if(length >= 5 && length < 25) {
            $('li.p_len').css('color', 'green');
            errors['password_length'] = 0;}
        else {
            $('li.p_len').css('color', 'tomato');
            errors['password_length'] = 1;}

        //#2 russian language
        if(russian.test(password.value)) {
            $('li.p_rus').css('color', 'tomato');
            errors['password_rus'] = 1;}
        else{
            $('li.p_rus').css('color', 'green');
            errors['password_rus'] = 0;}

        //#3 spec symbols
        if(spec_password.test(password.value)){
            $('li.p_spec').css('color', 'tomato');
            errors['password_symbols'] = 1;}
        else{
            $('li.p_spec').css('color', 'green');
            errors['password_symbols'] = 0;}
    });
});

var submit_login = document.getElementById('submit_login');
submit_login.onclick = sendAjaxData;

function sendAjaxData() {
	var sum_errors = 0;
	for(var key in errors){
	  if(errors.hasOwnProperty(key) && !isNaN(errors[key])) {
	    sum_errors += parseInt(errors[key], 10);
	  }
	}
	console.log(sum_errors);
    if(sum_errors == 0){
        $.post('/login_ajax', {
            login: login.value,
            password: password.value
        }, function(data){
            if(data === 1){
			    swal('logined');
                window.location.replace("/admin/main");
            }
            else if(data === 2){
			    swal('wrong password');
            }
            else if(data === 3){
			    swal('wrong login');
            }
        });
    }
    else{
        var error_s = '';
        switch (sum_errors) {
          case 1:
            error_s = 'error';
            break;
          default:
            error_s = 'errors';
        }
        swal('correct errors','you have ' + sum_errors.toString() + ' ' + error_s.toString());
    }
}