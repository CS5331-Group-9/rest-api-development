var API_ENDPOINT = "http://192.168.33.10:8080";
var WEB_BASEURL = "http://192.168.33.10:80";

$('#login-btn').click(function () {
    var user_info = {
        'username' : $('#username').val(),
        'password' : $('#password').val()
    };

    $.ajax({
        url: API_ENDPOINT + '/users/authenticate',
        data: user_info,
        type: 'post',
        success : function (response) {
            if (response.status == true){
                window.sessionStorage.token = response.token;
                location.replace(WEB_BASEURL + "/public_diary.html");
            } else {
                alert("Wrong username or password");
            }
        }
    });
});