
$(document).ready(function() {
    $(".toggle_more").click(function(event) {
        $(this).hide();
        $(this).siblings().show();
        $(this).parent().next(".more_details").slideDown(200);
    })
    $(".toggle_less").click(function(event) {
        $(this).hide();
        $(this).siblings().show();
        $(this).parent().next(".more_details").slideUp(200);
    })
})