var API_ENDPOINT = "http://192.168.33.10:8080";
var WEB_BASEURL = "http://192.168.33.10";

$(document).ready(function () {
    $(".del-clicked").click(function (event) {
        id = parseInt(event.target.id.replace('del_', ''))
        console.log('id: ',id);
        
        $.ajax({
            url: API_ENDPOINT + '/diary/delete',
            data: {
                token: window.sessionStorage.token,
                id:id,
            },
            type: 'post',
            success: function (response) {
                console.log('response: ', response);
                if (response.status) {
                    alert('Successfully deleted!')
                    location.reload()
                }else{
                    alert('Could not delete diary')
                }
            }
        });

    })
    $(".toggle-clicked").change(function (event) {
        var self = $("#"+event.target.id)
        id = parseInt(event.target.id.replace('toggle_', ''))
        var toggle_val = self.prop('checked')
        $.ajax({
            url: API_ENDPOINT + '/diary/permission',
            data: {
                token: window.sessionStorage.token,
                id:id,
                public:toggle_val,
            },
            type: 'post',
            success: function (response) {
                console.log('response: ', response);
                if (response.status) {

                }else{
                    self.prop('checked', !toggle_val).bootstrapToggle('destroy').bootstrapToggle();
                    alert('Could not toggle permission')
                }
            }
        });

    })
})