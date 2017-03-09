(function(){
    var templateSelect = $("#id_template");
    var toggleCustomTemplateTable = function(){
        var templateForm = $("[custom-template-table]");
        templateForm.toggle(templateSelect.val() === "custom");
        $("#id_DateGetter").prop('disabled', templateSelect.val() !== "custom");
        $("#id_DescriptionGetter").prop('disabled', templateSelect.val() !== "custom");
        $("#id_AmountGetter").prop('disabled', templateSelect.val() !== "custom");
    };
    toggleCustomTemplateTable();
    templateSelect.on("change", toggleCustomTemplateTable);

    var hasBalanceCheckbox = $("#id_has_balance");
    var enableDisableBalanceInput = function(){
        $("#id_CurrentBalanceGetter").prop('disabled', !hasBalanceCheckbox.is(":checked"));
    };
    enableDisableBalanceInput();
    hasBalanceCheckbox.on('change', enableDisableBalanceInput);

    var hasOtherDate1Checkbox = $("#id_has_other_date_1");
    var enableDisableOtherDate1Inputs = function(){
        $("#id_OtherDate1Name").prop('disabled', !hasOtherDate1Checkbox.is(":checked"));
        $("#id_OtherDate1Getter").prop('disabled', !hasOtherDate1Checkbox.is(":checked"));
    };
    enableDisableOtherDate1Inputs();
    hasOtherDate1Checkbox.on('change', enableDisableOtherDate1Inputs);

    var hasOtherString1Checkbox = $("#id_has_other_string_1");
    var enableDisableOtherString1Inputs = function(){
        $("#id_OtherString1Name").prop('disabled', !hasOtherString1Checkbox.is(":checked"));
        $("#id_OtherString1Getter").prop('disabled', !hasOtherString1Checkbox.is(":checked"));
    };
    enableDisableOtherString1Inputs();
    hasOtherString1Checkbox.on('change', enableDisableOtherString1Inputs);
})();
