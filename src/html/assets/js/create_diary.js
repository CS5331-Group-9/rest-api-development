var API_ENDPOINT = "http://192.168.33.10:8080";
var WEB_BASEURL = "http://192.168.33.10:80";

$('#submit-diary').click(function () {
    var new_diary = {
        token: window.sessionStorage.token,
        title: $('#diary-title').val(),
        public: $('#isPublic').prop('checked'),
        text: $('#diary-text').val(),
    };
    console.log('new_diary: ', new_diary);
    if (!new_diary.title ||
        !new_diary.text) {
        alert("You cannot leave empty fields")
    } else {
        $.ajax({
            url: API_ENDPOINT + '/diary/create',
            data: new_diary,
            type: 'post',
            success: function (response) {
                console.log(response)
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