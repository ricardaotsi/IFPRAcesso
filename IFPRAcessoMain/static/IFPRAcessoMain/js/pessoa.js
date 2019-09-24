$(document).ready(function () {
    $('.ano').mask("0000");
    $('.matricula').mask("000000000000");
    $('.cracha').mask("00000000");
    $('.nome').mask('Z',{translation: {'Z': {pattern: /[a-zA-Z ]/, recursive: true}}});
    if($('.alert').hasClass('alert-success')){
        setTimeout(
            function() 
            {
                document.location.href="/";
            }, 4000);
    }
});