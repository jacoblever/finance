rome(document.getElementById('id_date_from'),{inputFormat: "YYYY-MM-DD"});
rome(document.getElementById('id_date_to'),{inputFormat: "YYYY-MM-DD"});

$('form[filter-form]').find('li').each(function(i, item){
    var li = $(item);
    var x = $('<a href="javascript:0">X</a>')
    li.find('label').append(" ").append(x);
    x.click(function(e){
        li.find(':input').val("");
        li.find(':input').focus();
    });
});

$('button[download-button]').click(function(){
    var values = $('[filter-form]').serialize();
    window.location.href = './download/?page=all&' + values;
});

$('button[clear-filter-button]').click(function(){
    var pageInput = $(this).closest("form").find("input[name=page]");
    if(pageInput.length > 0 && pageInput.val() === "all"){
        window.location.href = './?page=all';
    } else {
        window.location.href = './';
    }
});

var $transactionsForm = $('[transactions-form]');

$('[bulk-form]').find(':input').change(function(event){
    var namePostfix = $(event.target).attr('name');
    var $inputs = $transactionsForm.find(':input[name$="' + namePostfix + '"]');
    $inputs.val($(event.target).val()).change();
});

$transactionsForm.find(':input').change(function(e) {
    $(this).attr('changed', 'true');
});

function gotoPage(i) {
    window.location = updateQueryString("page", i == 1 ? null : i);
}

window.onbeforeunload = function(){
    if($transactionsForm.find(':input[changed=true]').length > 0) {
        return true;
    }
};

$('button[reset-button]').click(function(event) {
    // It's safe to repload now
    window.onbeforeunload = null;
    window.location.reload();
});

$transactionsForm.submit(function() {

    $("body").append("<div class='saving-overlay'>Saving...</div>");

    var data = $transactionsForm.find('input[name=csrfmiddlewaretoken]').serializeArray()

    var test = $transactionsForm.find(':input[changed=true]');
    test.parents('tr').each(function(i, tr) {
        var thisData = $(tr).find(':input').serializeArray();
        for(var i = 0; i < thisData.length; i++) {
            data.push(thisData[i]);
        }
    });

    var rowCount = data.filter(function(x){return x.name === 'id'}).length;
    console.log('Saving ' + rowCount + ' transactions...');
    var startTime = performance.now();

    $.ajax({
        type: $transactionsForm.attr('method'),
        url:  $transactionsForm.attr('action'),
        data:  data
    }).done(function(data) {
        var endTime = performance.now();
        console.log('Saved taking ' + (endTime-startTime)/1000 + ' ms.');
        console.log('Reloading...');
        setTimeout(function(){
            // It's safe to repload now
            window.onbeforeunload = null;
            window.location.reload();
        }, 500);
    });
    return false;
});

function updateQueryString(key, value) {
    var url = window.location.href;
    var re = new RegExp("([?&])" + key + "=.*?(&|#|$)(.*)", "gi"),
        hash;

    if (re.test(url)) {
        if (typeof value !== 'undefined' && value !== null) {
            return url.replace(re, '$1' + key + "=" + value + '$2$3');
        } else {
            hash = url.split('#');
            url = hash[0].replace(re, '$1$3').replace(/(&|\?)$/, '');
            if (typeof hash[1] !== 'undefined' && hash[1] !== null)
                url += '#' + hash[1];
            return url;
        }
    } else {
        if (typeof value !== 'undefined' && value !== null) {
            var separator = url.indexOf('?') !== -1 ? '&' : '?';
            hash = url.split('#');
            url = hash[0] + separator + key + '=' + value;
            if (typeof hash[1] !== 'undefined' && hash[1] !== null)
                url += '#' + hash[1];
            return url;
        } else {
            return url;
        }
    }
}
