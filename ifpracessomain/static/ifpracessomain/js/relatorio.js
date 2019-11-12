$(document).ready(function () {
    // var doc = new jsPDF();
    // $('.exportar').click(function () {   
    //     doc.fromHTML($('.content').html(), 15, 15, {
    //         'width': 170,
    //     });
    //     doc.save('sample-file.pdf');
    // });
    $('.exportar').click(function CreatePDFfromHTML() {
        let doc = new jsPDF('p','mm','a4');
        doc.addHTML($('.html-content'),function() {
            doc.save('relatorio.pdf');
        });
    });
});