var API_ENDPOINT = "http://192.168.33.10:8080";
var WEB_BASEURL = "http://192.168.33.10:80";

$('#register-btn').click(function () {
    var user_info = {
        'username' : $('#username').val(),
        'password' : $('#password').val(),
        'fullname' : $('#fullname').val(),
        'age' : $('#age').val()
    };

    $.ajax({
        url: API_ENDPOINT + '/users/register',
        data: user_info,
        type: 'post',
        success : function (response) {
            if (response.status == true){
                alert("Registration success!");
                location.replace(WEB_BASEURL + "/login/login.html");
            }

            var error_string = "Error:\n\r";

            if (!$.isEmptyObject(response.error)){
                $.each(response.error, function( index, value ) {
                    error_string += value + "\n\r";
                });

                alert(error_string);
            }

        }
    });
});