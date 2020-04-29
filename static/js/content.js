$(document).ready(function(){
    console.log("I am now here");
    console.log(pageData.stylesheets[0])
    pageData.stylesheets.forEach(addCss);
});

function addCss(fileName, index) {
    var link = $("<link />",{
        rel: "stylesheet",
        type: "text/css",
        href: "static/css/"+fileName
    })
    $('head').append(link);
}