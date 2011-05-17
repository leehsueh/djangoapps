var books = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation"
    ];

re = new RegExp(/[12]?[A-Za-z ]+[A-Za-z] ?[0-9]+:[0-9]+ ?(- ?[0-9]+(:[0-9]+)?)?$/);

add_input_text = function(event) {
    event.preventDefault();
    var newLiNode = $("#cross_refs li").last().clone();
    newLiNode.children("input.cf").val("");
    $("#cross_refs").append(newLiNode);
    $("#cross_refs a").click(remove_input_text);
    $("#cross_refs input.cf").last().autocomplete({
        source: books
    });
    reset_form_validation();
}

remove_input_text = function(event) {
    event.preventDefault();
    var liItem = $(this).parentsUntil("ul");
    if (liItem.siblings().length < 1) {
        liItem.children("input").val("");
    } else {
        // animate/remove list item
        liItem[0].style.visibility = 'hidden';
        liItem.animate({
                    opacity: 0,
                    height: 0
                  }, 300, function() {liItem.remove();});
    }
    reset_form_validation();
}

function reset_form_validation() {
    $("form").validator({
        position: 'top left',
        offset: [-12, 0],
        message: '<div><em/></div>', // em element is the arrow
        messageAttr: 'data-message'
    });
}

function split( val ) {
    return val.split( /,\s*/ );
}
function extractLast( term ) {
    return split( term ).pop();
}

$(document).ready(function() {
    // initial event binding
    $("button").click(add_input_text);
    $("#cross_refs a").click(remove_input_text);
    $("#cross_refs input.cf").autocomplete({
        source: books
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
    reset_form_validation();
})