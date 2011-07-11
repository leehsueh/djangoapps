/*
 * NT Greek Vocabulary
 * Javascript interaction on the list words page (listcards.html).
 */

$(document).ready(function() {
    var filter_words = function(event) {
        delay = 300;
        event.preventDefault(); // prevent link from navigating
        className = $(this).text();
        if (parseInt(className)) {  // lesson number
            className = 'ln' + className;
        }
        if (className == 'NA')
            className = 'ln';

        // select or clear?
        if ($(this).is(".selected")) {
            $(this).removeClass("selected");
            $(this).removeAttr("title");
            // get current filter
            keepFilter = $(".selected").text();
            if (parseInt(keepFilter))
                keepFilter = 'ln' + keepFilter;

            if (keepFilter) {
                keepFilter = "." + keepFilter;
            }
            $(".greekword" + keepFilter).fadeIn(delay);
        } else {    // select
            $(this).parent().siblings().children().removeClass("selected");    // unselect others
            $(this).parent().siblings().children().removeAttr("title");
            // get current filter
            keepFilter = $(".selected").text();
            if (parseInt(keepFilter))
                keepFilter = 'ln' + keepFilter;
            if (keepFilter) {
                keepFilter = "." + keepFilter;
            }
            $(this).addClass("selected");
            $(this).attr("title", "Click to unselect")
            // further restrict visible words
            $(".greekword").not("." + className).fadeOut(delay);
            $(".greekword" + keepFilter + "." + className).fadeIn(delay);
        }
    }
    $(".pos_filter").click(filter_words);
    $(".lesson_filter").click(filter_words);

    $("#fixedbottom > div > h2").click(function() {
        if ($(this).find("span").text() == "[+]") {
            $(this).find("span").empty();
            $(this).find("span").append("[-]");
        } else {
            $(this).find("span").empty();
            $(this).find("span").append("[+]");
        }
        $(this).next(".inline_list").slideToggle(200);
        //$("#letters .inline_list").slideToggle(300);
    });

    $("#lessons .inline_list").hide();
    $("#parts_of_speech .inline_list").hide();
    $("#letters .inline_list").show();  // default expand letters
    // add animated scrolling when clicking on a letter
    $("#letters .inline_list li a").click(function() {
        var elementClicked = $(this).attr("href");
        var destination = $(elementClicked).offset().top;
        $("html:not(:animated),body:not(:animated)").animate({scrollTop: destination-20}, 800);
        return false;
    });

    $("section").hover(
        function() {
            //$(this).children("h1").css("background-color","#f6f6f6");
            $(this).children("h1").css("color","#222");
        },
        function() {
            //$(this).children("h1").css("background-color","");
            $(this).children("h1").css("color","");
        }
    );
    $(".greekword").hover(
        function() {
            $(this).children("a").addClass("roundedborderhover");
            $(this).children("span").removeClass("hidden");
        },
        function() {
            $(this).children("a").removeClass("roundedborderhover");
            $(this).children("span").addClass("hidden");
        }
    );
});