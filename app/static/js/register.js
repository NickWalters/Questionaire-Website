/**
 * JS Client-sided form validation
 */
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
            /** Check if username already in use
            var error = $("#errorusername")
            if() {
                error.html("");
            }
            else {
                error.css("color","red");
                error.html("User name has been used.");
            }

            */
        }
    });
    return
}

/**
 * Form email address format checking
 */
function email(){
    var emailSubmitted = $( "#email" ).val();
    var check = new RegExp('^[a-z0-9.]+@[a-z0-9.-]+\\.[a-z]{2,}$');
    var error = $("#erroremail")
    if (check.test(emailSubmitted)) {
        error.css("color","green");
        error.html("Email is valid");
    }
    else {
        error.css("color","red");
        error.html("This email is not valid");
    }
    return;
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
    var error = $("#errorpassword2")
    if($( "#password" ).val() == $( "#password2" ).val()){
        error.css("color","green");
        error.html("");
    }
    else {
        error.css("color","red");
        error.html("Field must be equal to password");

    }
    return
}