(function(){
    var templateSelect = $("#id_template");
    var toggleCustomTemplateTable = function(){
        var templateForm = $("[custom-template-table]");
        templateForm.toggle(templateSelect.val() === "custom");
        $("#id_get_date").prop('disabled', templateSelect.val() !== "custom");
        $("#id_get_description").prop('disabled', templateSelect.val() !== "custom");
        $("#id_get_amount").prop('disabled', templateSelect.val() !== "custom");
    };
    toggleCustomTemplateTable();
    templateSelect.on("change", toggleCustomTemplateTable);

    var hasBalanceCheckbox = $("#id_has_balance");
    var enableDisableBalanceInput = function(){
        $("#id_get_current_balance").prop('disabled', !hasBalanceCheckbox.is(":checked"));
    };
    enableDisableBalanceInput();
    hasBalanceCheckbox.on('change', enableDisableBalanceInput);

    var hasOtherDate1Checkbox = $("#id_has_custom_date_1");
    var enableDisableOtherDate1Inputs = function(){
        $("#id_custom_date_1_name").prop('disabled', !hasOtherDate1Checkbox.is(":checked"));
        $("#id_get_custom_date_1").prop('disabled', !hasOtherDate1Checkbox.is(":checked"));
    };
    enableDisableOtherDate1Inputs();
    hasOtherDate1Checkbox.on('change', enableDisableOtherDate1Inputs);

    var hasOtherString1Checkbox = $("#id_has_custom_text_1");
    var enableDisableOtherString1Inputs = function(){
        $("#id_custom_text_1_name").prop('disabled', !hasOtherString1Checkbox.is(":checked"));
        $("#id_get_custom_text_1").prop('disabled', !hasOtherString1Checkbox.is(":checked"));
    };
    enableDisableOtherString1Inputs();
    hasOtherString1Checkbox.on('change', enableDisableOtherString1Inputs);
})();
