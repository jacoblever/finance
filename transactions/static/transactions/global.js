(function(){
    function startLongAction(message){
        var overlay = $("<div class='loading-overlay'>" + message + "</div>");
        $("body").append(overlay);
        return {
            done: function(){
                overlay.remove();
            }
        }
    }

    window.global = {
        startLongAction: startLongAction
    }
})();
