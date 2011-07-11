
$(document).ready(function() {
    $(".toggle_more").click(function(event) {
        $(this).hide();
        $(this).siblings().show();
        $(this).parent().next(".more_details").fadeIn(500);
    })
    $(".toggle_less").click(function(event) {
        $(this).hide();
        $(this).siblings().show();
        $(this).parent().next(".more_details").fadeOut(200);
    })
})