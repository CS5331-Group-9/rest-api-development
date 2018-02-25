var API_ENDPOINT = "http://192.168.33.10:8080"

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
                location.replace(API_ENDPOINT + "/diary");
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