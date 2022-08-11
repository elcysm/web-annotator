function keepData(){
    // $("#name").val = document.getElementsByName("#username").value = "hello"
    // document.getElementsByClassName(".username").innerHTML = "Hello";
    $(".username").val("Hiii");
}
function add_modal(){

    $('#addModal').modal('toggle'); 

}
function develop(){
    alert("Chức năng này đang phát triển!")
}
   var opacity = 0;
   var intervalID = 0;
   window.onload = fadeIn;
   
   function fadeIn() {
       setInterval(show, 50);
   }
   
   function show() {
       var body = document.getElementById("fade");
       opacity = Number(window.getComputedStyle(body)
                           .getPropertyValue("opacity"));
       if (opacity < 1) {
           opacity = opacity + 0.1;
           body.style.opacity = opacity
       } else {
           clearInterval(intervalID);
       }
   }
    
    $("#fade").fadeTo(3000, 500).slideUp(500, function(){
    $("#fade").slideUp(500);
});

    $(document).ready(function() {
        $("#fade").hide();
        $("#fade").fadeTo(3000, 500).slideUp(500, function() {
            $("#fade").slideUp(500);
        });
    });



(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
 
      

})(jQuery);




var current = location.pathname;
$('.nav .nav-link').each(function(){
    var $this = $(this);
    // if the current path is like this link, make it active
    if($this.attr('href').indexOf(current) !== -1){
        $this.addClass('active');
    }
})
