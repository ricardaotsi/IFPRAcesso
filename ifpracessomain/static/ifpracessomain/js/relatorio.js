$(document).ready(function () {
    var registros = $( ".registro" )
    
    $('.exportar').click(function CreatePDFfromHTML() {
        var doc = new jsPDF('p', 'mm', 'a4');
        doc.autoTable({
            html: '.table'
        });

        doc.save('relatorio.pdf');
    });

    $('.filtrar').click(function(event){
        event.preventDefault();
        $( ".registro" ).each(function( ) {
            $(this).remove()
        });
        registros.each(function( ) {
            $(".tabela").append($(this))
        });
        var inicio = new Date($(".dt_inicio")[0].value);
        var fim = new Date($(".dt_fim")[0].value);
        if (inicio.length != 0 && fim.length == 0){
            $( ".registro" ).each(function(  ) {
                y=$(this)[0].children[2].textContent.substring(6,10);
                m=$(this)[0].children[2].textContent.substring(3,5);
                d=$(this)[0].children[2].textContent.substring(0,2);
                var date_test = new Date(y.concat("-",m,"-",d));
                if(date_test<inicio){
                    $(this).remove();
                }
            });
        }else if(inicio.length != 0 && fim.length != 0){
            $( ".registro" ).each(function(  ) {
                y=$(this)[0].children[2].textContent.substring(6,10);
                m=$(this)[0].children[2].textContent.substring(3,5);
                d=$(this)[0].children[2].textContent.substring(0,2);
                var date_test = new Date(y.concat("-",m,"-",d));
                if(date_test<inicio || date_test>fim){
                    $(this).remove();
                }
            });
        }
    });
});