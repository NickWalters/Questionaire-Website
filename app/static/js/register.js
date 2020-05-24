
$(document).ready(function() {
    $( "#username" ).keyup(function() {
        username();
    });
    $( "#email" ).keyup(function() {
        email();
    });
    $( "#password" ).keyup(function() {
        password();
    });
    $( "#password2" ).keyup(function() {
        password2();
    });
});

/**
 * Form email address format checking
 */
function email(){
    var emailSubmitted = $( "#email" ).val();
    var check = new RegExp('^[a-z0-9.]+@[a-z0-9.-]+\\.[a-z]{2,}$');
    if (check.test(emailSubmitted)) {
        /**THIS IS A VALID EMAIL */
    }
    else {
        //valid.style.color="red";
            //valid.innerHTML="not a valid email";
        /**THIS IS A NOT VALID EMAIL */
    }
    return;
}

/**
 * Form username AJAX
 */
function username(){
    var usernameSubmitted = $( "#username" ).val();
    var url = ""; //AJAX request URL

    $.ajax({
        type: 'GET',
        url: url,
        data: { get_param: 'value' }, 
        dataType: 'json',
        success: function (data) {
            /**DO STUFF */
        }
    });
    return
}

/**
 * Form password checking
 */
function password(){
    return
}

/**
 * Form password2 checking
 */
function password2(){
    console.log($( "#password" ).val())
    console.log($( "#password2" ).val())
    if($( "#password" ).val() == $( "#password2" ).val()){
        console.log("PASSWORDS equal")
    }
    return
}