$(document).ready(function () {
    /**
     * Mascara de campos
     */
    $('.ano').mask("0000");
    $('.matricula').mask("000000000000");
    $('.cracha').mask("00000000");
    $('.nome').mask('Z',{translation: {'Z': {pattern: /[a-zA-Z ]/, recursive: true}}});
});

$(".pessoa").submit(function(event){
    $(".btn-pessoa").append("  <span class='spinner-border spinner-border-sm'></span>");
});