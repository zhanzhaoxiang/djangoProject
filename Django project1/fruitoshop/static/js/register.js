$(function() {
     var error_name = false;
     var error_password = false;
     var error_check_password = false;
     var error_email = false;
     var error_check = false;
     var error_age = false;
     var error_phone = false;

     $('#username').blur(function() {
         check_user_name();
     });
     $('#age').blur(function() {
         check_age();
     });
     $('#password').blur(function() {
         check_pwd();
     });
     $('#repassword').blur(function() {
         check_cpwd();
     });
     $('#phone').blur(function() {
         check_phone();
     })
     $('#email').blur(function() {
         check_email();
     });
     $('#allow').click(function() {
         if ($(this).is(':checked')) {
             error_check = false;
             $(this).siblings('span').hide();
         } else {
             error_check = true;
             $(this).siblings('span').html('请勾选同意');
             $(this).siblings('span').show();
         }
     });

     function check_user_name() {
         var len = $('#username').val().length;
         $('#username').next().css('color', 'red');
         if (len < 5 || len > 20) {
             $('#username').next().html('请输入5-20个字符的用户名')
             $('#username').next().show();
             error_name = true;
             return;
         } else {
             $.getJSON('/register_exist/', {'username': $('#username').val()}, function (data) {
             if (data.count !== 0) {
                 $('#username').next().html('用户名已存在')
                 $('#username').next().show();
                 error_name = true;

             } else {
                 $('#username').next().html('用户名可用')
                 $('#username').next().show();
                 $('#username').next().css('color', 'green');
                 error_name = false;
             }
         })
         }

     }

     function check_age() {
         var len = parseInt($('#age').val());
         $('#age').next().css('color', 'red');
         if (len < 1 || len > 200) {
             $('#age').next().html('请输入正确年龄')
             $('#age').next().show();
             error_age = true;
             return;
         } else {
             $('#age').next().html('年龄可用')
             $('#age').next().show();
             $('#age').next().css('color', 'green');
             error_age = false;
         }
     }

     function check_phone() {
         var len = $(' #phone').val().length;
         $('#phone').next().css('color', 'red');
         if (len != 11){
             $('#phone').next().html(' 请输入正确的手机号码')
             $('#phone').next().show();
             error_phone = true;
             return;
         } else {
             $('#phone').next().html('手机号可用')
             $('#phone').next().show();
             $('#phone').next().css('color', 'green');
             error_phone = false;
         }
     }

     function check_pwd() {
         var len = $('#password').val().length;
         if (len < 8 || len > 20) {
             $('#password').next().html('密码最少8位，最长20位')
             $('#password').next().show();
             error_password = true;
         } else {
             $('#password').next().hide();
             error_password = false;
         }
     }

     function check_cpwd() {
         var pass = $('#password').val();
         var cpass = $('#repassword').val();
         if (pass != cpass) {
             $('#repassword').next().html('两次输入的密码不一致')
             $('#repassword').next().show();
             error_check_password = true;
         } else {
             $('#repassword').next().hide();
             error_check_password = false;
         }
     }

     function check_email() {
         var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
         if (re.test($('#email').val())) {
             $('#email').next().hide();
             error_email = false;
         } else {
             $('#email').next().html('你输入的邮箱格式不正确')
             $('#email').next().show();
             error_email = true;
         }
     }

     $('#reg_form').submit(function() {
         check_user_name();
         check_pwd();
         check_cpwd();
         check_email();
         if (error_name == false && error_age ==false && error_phone == false && error_password == false && error_check_password == false && error_email == false && error_check == false) {
             return true;
         } else {
             return false;
         }
     });
})