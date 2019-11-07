
document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('[type="file"]').onchange = changeEventHandler;
}, false);

function changeEventHandler(event) {
    $(".custom-file-label").text($('#inputGroupFile01')[0].value.split(/(\\|\/)/g).pop());
}


