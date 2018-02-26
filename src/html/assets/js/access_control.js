var API_ENDPOINT = "http://192.168.33.10:8080";
var WEB_BASEURL = "http://192.168.33.10";
var loginRequired = ["logout.html", "private_diary.html", "create_diary.html"];

var token = window.localStorage.token;
var currentPath = window.location.pathname+window.location.search;
currentPath = currentPath.replace("/", "");

if (token === undefined && loginRequired.indexOf(currentPath) !== -1){
    alert("Please login first");
    location.replace(window.location.origin + "/login.html");
}