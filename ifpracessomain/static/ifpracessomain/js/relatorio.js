$(document).ready(function () {
    $('.exportar').click(function CreatePDFfromHTML() {
        let doc = new jsPDF('p','mm','a4');
        doc.addHTML($('.html-content'),function() {
            doc.save('relatorio.pdf');
        });
    });
});