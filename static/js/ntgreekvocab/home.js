/*
 * NT Greek Vocabulary
 * Javascript interaction on the HOME page (home.html).
 */
$(document).ready(function() {
    // clear lesson filter ajax logic
    $("#lesson_filters a").click(function() {
        $.ajax({
          url: "/ntgreek/clearln",
          type: "GET",
          success: function(html){
            $("#lesson_filters p").text(html);
          }
        });
    })

    // show/hide word info
    var toggle_show_hide_link = function(event) {
        event.preventDefault();
        if ($(this).text() == "[-] Hide") {
            $("#word_info").animate({
                opacity: 0,
                height: 'toggle'
              }, 300);
            $("#word_info").slideUp(200);
            $(this).empty();
            $(this).append("[+] Show");
        } else {
            $("#word_info").animate({
                opacity: 1,
                height: 'toggle'
              }, 300);
            $(this).empty();
            $(this).append("[-] Hide");
        }
    }

    $("#toggle_info_link").click(toggle_show_hide_link);
    //$("#word_info").hide();

    $("article header h1 a").mouseenter(
        function () {
            $(this).addClass("rollover");
            //$(this).animate({opacity: 0.40},0);
            $("#feedback_text").removeClass("hidden");
        });
    $("article header h1 a").mouseleave(
        function () {
            $(this).removeClass("rollover");
            //$(this).animate({opacity: 1}, 200);
            $("#feedback_text").addClass("hidden");
        }
    );
    $("#feedback_text").addClass("hidden");
});


