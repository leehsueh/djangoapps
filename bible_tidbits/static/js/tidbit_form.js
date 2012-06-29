re = new RegExp(/[12]?[A-Za-z ]+[A-Za-z] ?[0-9]+:[0-9]+ ?(- ?[0-9]+(:[0-9]+)?)?$/);

function get_bible_text(input_elem) {
    passage = $(input_elem).val();
    if (passage != null && re.test(passage)) {
        console.log(passage);
        $("#passage_preview").text("Loading " + passage);
        $.get(
            "/tidbits/ajax/bible_text/",
            {passage: passage},
            function(data) {
                $("#passage_preview").text(data);
            }
        );
    } else if (passage == '') {
        $("#passage_preview").text("Enter a passage");
    } else {
        $("#passage_preview").text("Specify verses.");
    }
}

add_input_text = function(event) {
    event.preventDefault();
    var newLiNode = $("#cross_refs li").last().clone();
    var inputElem = newLiNode.children("input.cf");
    inputElem.val("");
    inputElem.focus(add_cf_on_focus);
    $("#cross_refs").append(newLiNode);
    $("#cross_refs a").click(remove_input_text);
    $("#cross_refs input.cf").last().autocomplete({
        source: books
    })
    .keyup(bible_text_mouseover_trigger)
    .focus(bible_text_mouseover_trigger);
    reset_form_validation();
}

remove_input_text = function(event) {
    event.preventDefault();
    var liItem = $(this).parentsUntil("ul");
    if (liItem.siblings().length < 1) {
        liItem.children("input").val("");
    } else {
        // animate/remove list item
        liItem.children("a").remove();  // prevent line break forming when width shrinks
        liItem.animate({
                    opacity: 0,
                    width: 0
                  }, 300, function() {liItem.remove();});
    }
    reset_form_validation();
}

function add_cf_on_focus(event) {
    if ($(this).parentsUntil("ul").next().length == 0)
        add_input_text(event);
}

function reset_form_validation() {
    $("form").validator({
        position: 'top left',
        offset: [-12, 0],
        message: '<div><em/></div>', // em element is the arrow
        messageAttr: 'data-message'
    });
}

function on_submit(event) {
    $("#cross_refs input.cf").first().attr("required", true);
}

// for tag autocomplete; multiple tags in single textarea
function split( val ) {
    return val.split( /,\s*/ );
}
// for tag autocomplete; multiple tags in single textarea
function extractLast( term ) {
    return split( term ).pop();
}

function bible_text_mouseover_trigger() {
    get_bible_text(this);
}

$(document).ready(function() {
    // initial event binding
    $("#cross_refs a").click(remove_input_text);
    $("#cross_refs input.cf").autocomplete({
        source: books
    });
    $("input.cf").focus(add_cf_on_focus);
    
    // bible preview setup
    $("input.cf").keyup(bible_text_mouseover_trigger);
    $("input.cf").focus(bible_text_mouseover_trigger);
    
    
    $("#toggle_more").click(function() {
       $(this).hide();
       $("#toggle_less").show();
       $("#more_details").slideDown(200);
    });
    $("#toggle_less").click(function() {
       $(this).hide();
       $("#toggle_more").show();
       $("#more_details").slideUp(200);
    });
    $("#tags")
    // don't navigate away from the field on tab when selecting an item
    .bind( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
                $( this ).data( "autocomplete" ).menu.active ) {
            event.preventDefault();
        }
    })
    .autocomplete({
        source: function( request, response ) {
					$.getJSON( "/tidbits/ajax/tags/", {
						term: extractLast( request.term )
					}, response );
				},
        search: function() {
            // custom minLength
            var term = extractLast( this.value );
            if ( term.length < 2 ) {
                return false;
            }
        },
        focus: function() {
            // prevent value inserted on focus
            return false;
        },
        select: function( event, ui ) {
            var terms = split( this.value );
            // remove the current input
            terms.pop();
            // add the selected item
            terms.push( ui.item.value );
            // add placeholder to get the comma-and-space at the end
            terms.push( "" );
            this.value = terms.join( ", " );
            return false;
        }
    });
    $("#save_btn").click(on_submit);
    reset_form_validation();

})

/* WYMEditor plugin */
/* Here we replace each element with class 'wymeditor'
 * (typically textareas) by a WYMeditor instance.
 *
 * We could use the 'html' option, to initialize the editor's content.
 * If this option isn't set, the content is retrieved from
 * the element being replaced.
 */
$(function() {
    $("input[id='save_btn']").addClass("wymupdate");
    $("#more").addClass("wymeditor");

    $('.wymeditor').wymeditor({
        skin:'compact',
        boxHtml:   "<div class='wym_box'>"
              + "<div class='wym_area_top'>"
              + WYMeditor.TOOLS
              //+ WYMeditor.CONTAINERS
              //+ WYMeditor.CLASSES
              + "</div>"
              + "<div class='wym_area_left'></div>"
              + "<div class='wym_area_right'>"
              + "</div>"
              + "<div class='wym_area_main'>"
              + WYMeditor.HTML
              + WYMeditor.IFRAME
              + WYMeditor.STATUS
              + "</div>"
              + "<div class='wym_area_bottom'>"
              + "</div>"
              + "</div>",
          toolsItems: [
                {'name': 'Bold', 'title': 'Strong', 'css': 'wym_tools_strong'},
                {'name': 'Italic', 'title': 'Emphasis', 'css': 'wym_tools_emphasis'},
                {'name': 'Superscript', 'title': 'Superscript', 'css': 'wym_tools_superscript'},
                {'name': 'Subscript', 'title': 'Subscript', 'css': 'wym_tools_subscript'},
                {'name': 'InsertOrderedList', 'title': 'Ordered_List', 'css': 'wym_tools_ordered_list'},
                {'name': 'InsertUnorderedList', 'title': 'Unordered_List', 'css': 'wym_tools_unordered_list'},
                {'name': 'Indent', 'title': 'Indent', 'css': 'wym_tools_indent'},
                {'name': 'Outdent', 'title': 'Outdent', 'css': 'wym_tools_outdent'},
                {'name': 'Undo', 'title': 'Undo', 'css': 'wym_tools_undo'},
                {'name': 'Redo', 'title': 'Redo', 'css': 'wym_tools_redo'},
                {'name': 'CreateLink', 'title': 'Link', 'css': 'wym_tools_link'},
                {'name': 'Unlink', 'title': 'Unlink', 'css': 'wym_tools_unlink'},
                {'name': 'Paste', 'title': 'Paste_From_Word', 'css': 'wym_tools_paste'},
                {'name': 'ToggleHtml', 'title': 'HTML', 'css': 'wym_tools_html'},
                {'name': 'Preview', 'title': 'Preview', 'css': 'wym_tools_preview'}
              ]
    });
});