var importForm = $('form[import-form]');
var accountSelect = importForm.find("select[name=account]");
var fileInput = importForm.find("input[name=file]");
var importButton = importForm.find("[import-button]");

var onInputChange = function(){
    importForm.find("input[name=actually-import]").remove();
    if(fileInput.val() !== "") {
        importForm.submit();
    } else {
        $("[import-preview]").empty();
    }
};

accountSelect.change(onInputChange);
fileInput.change(onInputChange);

importForm.submit(function() {
    var action = global.startLongAction("Loading...")
    importButton[0].disabled = true;
    $.ajax({
        type: importForm.attr('method'),
        url:  importForm.attr('action'),
        data:  new FormData(importForm[0]),
        cache: false,
        contentType: false,
        processData: false
    }).done(function(data) {
        $("[import-preview]").html(data);
        importButton[0].disabled = false;
        action.done();
    }).fail(function(data) {
        var newDoc = document.open("text/html", "replace");
        newDoc.write("<pre>" + data.responseText + "</pre>");
        newDoc.close();
    });

    return false;
});
