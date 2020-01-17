function popover_show()
{
    $("[data-toggle='popover']").popover().on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(".popover").on("mouseleave", function () {
            $(_this).popover('hide'); 
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide");
            }
        }, 300);
	});
}

$(document).ajaxSuccess( function(event, jqXHR, options){
    var rep = jqXHR.responseJSON
    var url = "/login/"
    if(rep.code == "301"){
        alert(rep.message);
        location.href = url;
    }
} );

