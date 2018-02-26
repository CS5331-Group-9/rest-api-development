//Login Page
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
                window.localStorage.token = response.token;
                location.replace(WEB_BASEURL + "/private_diary.html");
            } else {
                alert("Wrong username or password");
            }
        }
    });
});

//Register Page
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
                location.replace(WEB_BASEURL + "/login.html");
            }
            var error_string = "Error:\n\r";

            if (typeof response.error == "string"){
                alert(response.error);
            } else {
                if (!$.isEmptyObject(response.error)){
                    $.each(response.error, function( index, value ) {
                        error_string += value + "\n\r";
                    });

                    alert(error_string);
                }
            }
        }
    });
});

//Create Diary
$('#submit-diary').click(function () {
    var new_diary = {
        token: window.localStorage.token,
        title: $('#diary-title').val(),
        public: $('#isPublic').prop('checked'),
        text: $('#diary-text').val()
    };

    if (!new_diary.title ||
        !new_diary.text) {
        alert("You cannot leave empty fields")
    } else {
        $.ajax({
            url: API_ENDPOINT + '/diary/create',
            data: new_diary,
            type: 'post',
            success: function (response) {
                if (response.status == true) {
                    alert("Successfully created!")
                    location.replace(WEB_BASEURL + "/private_diary.html");
                } else {
                    alert("Could not create diary")
                }
            }
        });
    }
});

//Update Private Diary
$(document).ready(function () {
    $(".del-clicked").click(function (event) {
        var id = parseInt(event.target.id.replace('del_', ''));

        $.ajax({
            url: API_ENDPOINT + '/diary/delete',
            data: {
                token: window.localStorage.token,
                id:id
            },
            type: 'post',
            success: function (response) {
                if (response.status) {
                    alert('Successfully deleted!');
                    location.reload()
                }else{
                    alert('Could not delete diary');
                }
            }
        });

    });

    $(".toggle-clicked").change(function (event) {
        var self = $("#"+event.target.id);
        var id = parseInt(event.target.id.replace('toggle_', ''));
        var toggle_val = self.prop('checked');
        $.ajax({
            url: API_ENDPOINT + '/diary/permission',
            data: {
                token: window.localStorage.token,
                id:id,
                public:toggle_val
            },
            type: 'post',
            success: function (response) {
                if (response.status) {

                }else{
                    self.prop('checked', !toggle_val).bootstrapToggle('destroy').bootstrapToggle();
                    alert('Could not toggle permission')
                }
            }
        });

    })
});