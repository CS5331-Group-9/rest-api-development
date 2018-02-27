//Login Page
$('#login-btn').click(function () {
    var user_info = {
        'username' : escape($('#username').val()),
        'password' : escape($('#password').val())
    };

    $.ajax({
        url: API_ENDPOINT + '/users/authenticate',
        contentType: "application/json;",
        data: JSON.stringify(user_info),
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
        'username' : escape($('#username').val()),
        'password' : escape($('#password').val()),
        'fullname' : escape($('#fullname').val()),
        'age' : escape($('#age').val())
    };

    $.ajax({
        url: API_ENDPOINT + '/users/register',
        contentType: "application/json;",
        data: JSON.stringify(user_info),
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
        token: escape(window.localStorage.token),
        title: escape($('#diary-title').val()),
        public: escape($('#isPublic').prop('checked')),
        text: escape($('#diary-text').val())
    };

    if (!new_diary.title ||
        !new_diary.text) {
        alert("You cannot leave empty fields")
    } else {
        $.ajax({
            url: API_ENDPOINT + '/diary/create',
            contentType: "application/json;",
            data: JSON.stringify(new_diary),
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
            contentType: "application/json;",
            data: JSON.stringify({
                token: escape(window.localStorage.token),
                id:escape(id)
            }),
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
            contentType: "application/json;",
            data: JSON.stringify({
                token: escape(window.localStorage.token),
                id:escape(id),
                private:escape(!toggle_val)
            }),
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