$(function() {
    var error_username = false;
    var error_password = false;

    $("#username").blur(function() {
        check_username();
    });

    $("#password").focusout(function() {
        check_password();
    });

    function check_username() {
        var username_length = $("#username").val().length;

        if(username_length < 5 || username_length > 20) {
            $("#username").next().html("用户名长度必须在5至20之间");
            $("#username").next().show();
            error_username = true;
        } else {
            $("#username").next().hide();
            error_username = false;
        }
    }

    function check_password() {
        var password_length = $("#password").val().length;

        if(password_length < 8 || password_length > 20) {
            $("#password").next().html("密码长度必须在8至20之间");
            $("#password").next().show();
            error_password = true;
        } else {
            $("#password").next().hide();
            error_password = false;
        }
    }

    $("#login_form").submit(function() {
        check_username();
        check_password();

        if(error_username == false && error_password == false) {
            return true;
        } else {
            return false;
        }
    });
});