$(document).ready(function () {
    /**
     * Mascaras de campo
     */
    $('.ano').mask("0000");
    $('.matricula').mask("000000000000");
    $('.cracha').mask("00000000");
    $('.nome').mask('Z',{translation: {'Z': {pattern: /[a-zA-Z ]/, recursive: true}}});
});

/**
 * Função Django para obter o token de acesso para requisição POST AJAX
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Função Django para obter o token de acesso para requisição POST AJAX
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/**
 * Ao clicar em uma pessoa para alteração, salva a id da pessoa e redireciona para alteração
 */
$(".alterarpessoa").click(function(){
    var divnome = $(this).parent()[0]
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        url: '/ajax/update_session/',
        type: "POST",
        data: {
            'cracha': divnome.children[2].innerText,
        },
        dataType: 'json',
        success: function (result) {
            if(result.resultado==true){
                window.location.href="/pessoa/update/?identificador="+divnome.children[0].innerText+
                                    "&nome="+divnome.children[1].innerText+
                                    "&cracha="+divnome.children[2].innerText+
                                    "&matricula="+divnome.children[3].innerText+
                                    "&ano="+divnome.children[4].innerText+
                                    "&ativo="+divnome.children[5].innerText
            }
        },
    });
});