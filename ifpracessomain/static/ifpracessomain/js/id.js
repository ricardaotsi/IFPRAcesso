$(document).ready(function () {
    /**
     * Mascaras dos campos
     */
    $(".alerta-delete").hide();
    $(".alerta-insert").delay(1000).slideUp(1000);
    $('#identificador').mask('Z',{translation: {'Z': {pattern: /[a-zA-Z ]/, recursive: true}}});
});


/**
 * Aguarda um evento do mouse e deleta um identificador usando AJAX
 */
$(".btn-delete").click(function () {
    let identificador = $(this).parent().parent();
    let botao = $(this)[0]
    if ($(this)[0].childElementCount == 1)
        $(this).append("  <span class='spinner-border spinner-border-sm'></span>");
    if (confirm("Deseja realmente deletar o Identificador: " + identificador[0].innerText)) {
        $.ajax({
            url: '/ajax/deleteId/',
            type: "GET",
            data: {
                'identificador': $.trim(identificador[0].innerText),
            },
            dataType: 'json',
            success: function (result) {
                if(result.resultado==true){
                    identificador.fadeOut(1000);
                    setTimeout(
                        function() 
                        {
                            identificador.remove();
                            $("#mensagem").remove();
                            $(".alerta-delete").removeClass("alert-danger")
                            $(".alerta-delete").addClass("alert-success");
                            $(".alerta-delete").append("<strong id='mensagem'>Identificador deletado com sucesso</strong>");
                            $(".alerta-delete").slideDown(300).delay(2000).slideUp(1000);
                        }, 1000);
                }else{
                    botao.children[1].remove();
                    $("#mensagem").remove();
                    $(".alerta-delete").removeClass("alert-success");
                    $(".alerta-delete").addClass("alert-danger");
                    $(".alerta-delete").append("<strong id='mensagem'>Ocorreu um erro na operação</strong>");
                    $(".alerta-delete").slideDown(300).delay(2000).slideUp(1000);
                }
            },
            error: function (xhr) {
                botao.children[1].remove();
            },
        });
    }else{
        botao.children[1].remove();
    }
});