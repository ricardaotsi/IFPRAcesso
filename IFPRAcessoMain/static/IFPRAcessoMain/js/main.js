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
    if (urlAtual.attr("href").includes("pessoa")) {
        $(".cadastro").addClass("active");
    };
    if (urlAtual.attr("pathname") == "/") {
        $(".pesquisa").addClass("active");
    };
}