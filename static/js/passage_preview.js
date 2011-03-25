$(document).ready(function() {
    //book = $("#id_book").value;
    $("#passage_text").empty();
    $("#passage_text").append("Enter verse");
    
    var fetch_passage = function() {
        $("#refresh_link").hide();
        var book = $("#id_book").attr("value");
        var chapter = $("#id_chapter").attr("value");
        var startverse = $("#id_startverse").attr("value");
        var endverse = $("#id_endverse").attr("value");
        
        //$("#passage_text").append(book+' '+chapter+':'+startverse+'-'+endverse);
        if (book && chapter && startverse) {
            $.ajax({
                type: "GET",
                url: "/ajax/passage/"+book+"/"+chapter+"/"+startverse+"-"+endverse+"/",
                success: function(data) {
                    $(".loading_text").hide();
                    $("#passage_text").html(data);
                    $("#passage_text").slideDown(200);
                    //$("#refresh_link").show();
                }
            });
            
        } else {
            $("#passage_text").html("Missing parameters!");
            $("#passage_text").show();
            $("#refresh_link").show();
        }
        
    }
    var toggle_preview_link = function() {
        if ($(this).text() == "Hide Passage") {
            $(this).empty();
            $(this).append("Show Passage");
        } else {
            $(this).empty();
            $(this).append("Hide Passage");
        }
        $("#passage_preview").slideToggle(200);
        event.preventDefault();
    }
    var show_refresh_link = function() {
        $("#refresh_link").show();
    }
    
    $(".loading_text").ajaxStart(function() { $("#passage_text").hide(); $(this).show();});
    $("#refresh_link").click(fetch_passage);
    $("#preview_link").click(toggle_preview_link);
    $("#id_book").change(fetch_passage);
    $("#id_chapter").change(fetch_passage);
    $("#id_startverse").change(fetch_passage);
    $("#id_endverse").change(fetch_passage);
    $("#id_chapter").keypress(show_refresh_link);
    $("#id_startverse").keypress(show_refresh_link);
    $("#id_endverse").keypress(show_refresh_link);

    fetch_passage();
    $("#refresh_link").hide();
});

