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
    $.fn.fadeSlideToggle = function(speed, easing, callback) {
        $(this).animate({
            height: 'toggle',
            opacity: 'toggle'
        }, speed, easing, callback);
    };
    var toggle_show_hide_link = function(event) {
        event.preventDefault();
        $this = $(this);
        if ($this.text() == "[-] Hide") {
            $("section.word_info").fadeSlideToggle(300);
            $this.text("[+] Show");
        } else {
            $("section.word_info").fadeSlideToggle(300);
            $this.text("[-] Hide");
        }
    }

    $("#toggle_info_link").click(toggle_show_hide_link);
    //$("section.word_info").hide();

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


