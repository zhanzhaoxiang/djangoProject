$(function () {
    var error_phone = false;
    var error_code = false;
    var error_password = false;
    var error_check_password = false;

    $("#phone").blur(function () {
        check_phone();
    });

    $("#verification_code").focusout(function () {
        check_code();
    });

    $('#password').blur(function () {
        check_pwd();
    });
    $('#repassword').blur(function () {
        check_cpwd();
    });

    function check_phone() {
        var len = $(' #phone').val().length;
        $('#phone').next().css('color', 'red');
        if (len != 11) {
            $('#phone').next().html('号码格式错误')
            $('#phone').next().show();
            error_phone = true;
            return;
        } else {
            $('#phone').next().hide();
            error_phone = false;
        }
    }

    function check_code() {
        var code_length = $("#verification_code").val().length;

        if (code_length != 4) {
            $("#verification_code").next().html("验证码格式错误");
            $("#verification_code").next().show();
            error_code = true;
        } else {
            $("#verification_code").next().hide();
            error_code = false;
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

     $('#send_verification_code').click(function () {
         var phone = $('#phone').val();
         var reg = /^1[3-9]\d{9}$/;
         if (phone == '') {
             $('#phone').next().html('手机号码不能为空')
             $('#phone').next().show();
             error_phone = true;
         } else if (!reg.test(phone)) {
             $('#phone').next().html('手机号码格式错误')
             $('#phone').next().show();
             error_phone = true;
         } else {
             $('#phone').next().hide();
             error_phone = false;
         }
         var csrf = $("input[name='csrfmiddlewaretoken']").val()
         if (!error_phone) {
             $.ajax({
                 url: '/send_verification_code/',
                 type: 'POST',
                 data: {
                     'phone': phone,
                     'csrfmiddlewaretoken': csrf
                 },
                 success: function (data) {
                     if (data.msg== 'success') {
                         alert(data.msg);
                     } else {
                         alert(data.msg);
                     }
                 }
             })
         }
     })

    $("#login_form").submit(function () {
        check_phone();
        check_code();

        if (error_phone == false && error_code == false && error_password == false && error_check_password == false ) {
            return true;
        } else {
            return false;
        }
    });
});