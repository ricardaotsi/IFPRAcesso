$(document).ready(function () {
    $('.exportar').click(function CreatePDFfromHTML() {
        var doc = new jsPDF('p', 'mm', 'a4');
        doc.autoTable({
            html: '.table'
        });

        doc.save('table.pdf');
    });
});