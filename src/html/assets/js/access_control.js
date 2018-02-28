var API_ENDPOINT = "http://192.168.33.10:8080";
var WEB_BASEURL = "http://192.168.33.10";
var loginRequired = ["logout.html", "private_diary.html", "create_diary.html"];
var nonloginRequired = ["login.html", "register.html"];

var token = window.localStorage.token;
var currentPath = window.location.pathname+window.location.search;
currentPath = currentPath.replace("/", "");

function ajax_post(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            console.log('responseText:' + xmlhttp.responseText);
            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch(err) {
                console.log(err.message + " in " + xmlhttp.responseText);
                return;
            }
            callback(data);
        }
    };

    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader('Content-type', 'application/json');
    xmlhttp.send(data);
}

if (token === undefined && loginRequired.indexOf(currentPath) !== -1){
    alert("Please login first");
    location.replace(window.location.origin + "/login.html");
}

//auto login
if (token !== undefined && nonloginRequired.indexOf(currentPath) !== -1){
    ajax_post(API_ENDPOINT + '/users/validate', JSON.stringify({"token":token}), function(data) {
        if (data.status) {
            location.replace(WEB_BASEURL + "/private_diary.html");
        }
        else {
            window.localStorage.removeItem('token');
        }
    });
}