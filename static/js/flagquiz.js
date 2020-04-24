//Initiate when ready
$(document).ready(function(){
    console.log("Question number: 1");
    setPageData(1);
});

$(document).on("click", ".button", function(){
    question = parseInt($("#ajaxInput").html())+1;
    console.log("Question number: "+question);
    setPageData(question);
});

//Perform AJAX request
function setPageData(question){
    console.log(question)
    $("#ajaxInput").html(question);
    $("h4.questionHint").html("");
    $("#flag").attr("src","static/images/flag0"+question+".svg");
}