$(document).ready(function () {
    paginaAtual();
});

/**
 * função verificar em qual página estamos e mostrar na navbar
 */
function paginaAtual() {
    var urlAtual = $(location);
    $("ul.navbar-nav li.nav-item").each(function () {
        let $this = $(this);
        if ($this.hasClass("active")) {
            $this.removeClass("active");
        }
    });
    if (urlAtual.attr("href").includes("insertId")) {
        $(".cadastro").addClass("active");
    };
    if (urlAtual.attr("pathname") == "/") {
        $(".pesquisa").addClass("active");
    };
}

/**
 * Aguarda um evento do mouse e deleta um identificador usando AJAX
 */
$(".btn-delete").click(function () {
    let identificador = $(this).parent().parent();
    if ($(this)[0].childElementCount == 1)
        $(this).append("  <span class='spinner-border spinner-border-sm'></span>");
    if (confirm("Deseja realmente deletar o Identificador: " + $.trim(identificador.text()))) {
        $.ajax({
            url: '/ajax/deleteId/',
            data: {
                'identificador': $.trim(identificador.text())
            },
            dataType: 'json',
            success: function (result) {
                identificador.remove();
            }
        });
    }else{
        $(this)[0].children[1].remove();
    }
});