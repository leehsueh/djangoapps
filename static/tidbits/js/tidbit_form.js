var books = [
        "1 Chronicles",
        "1 Corinthians",
        "1 John",
        "1 Kings",
        "1 Peter",
        "1 Samuel",
        "1 Thessalonians",
        "1 Timothy",
        "2 Chronicles",
        "2 Corinthians",
        "2 John",
        "2 Kings",
        "2 Peter",
        "2 Samuel",
        "2 Thessalonians",
        "2 Timothy",
        "3 John",
        "Acts",
        "Amos",
        "Colossians",
        "Daniel",
        "Deuteronomy",
        "Ecclesiastes",
        "Ephesians",
        "Esther",
        "Exodus",
        "Ezekiel",
        "Ezra",
        "Galatians",
        "Genesis",
        "Habakkuk",
        "Haggai",
        "Hebrews",
        "Hosea",
        "Isaiah",
        "James",
        "Jeremiah",
        "Job",
        "Joel",
        "John",
        "Jonah",
        "Joshua",
        "Jude",
        "Judges",
        "Lamentations",
        "Leviticus",
        "Luke",
        "Malachi",
        "Mark",
        "Matthew",
        "Micah",
        "Nahum",
        "Nehemiah",
        "Numbers",
        "Obadiah",
        "Philemon",
        "Philippians",
        "Proverbs",
        "Psalms",
        "Revelation",
        "Romans",
        "Ruth",
        "Song of Solomon",
        "Titus",
        "Zechariah",
        "Zephaniah"

    ];
    
add_input_text = function(event) {
    event.preventDefault();
    //TODO: use jquery templates instead
    $("#cross_refs").append('<li><input type="text" name="cf" class="cf" placeholder="Enter passage"> <a>x</a></li>');
    $("#cross_refs a").click(remove_input_text);
    addCfRegExpValidation($("#cross_refs input[type=text]").last());
    $("#cross_refs input.cf").last().autocomplete({
        source: books
    });
}

remove_input_text = function(event) {
    event.preventDefault();
    var liItem = $(this).parentsUntil("ul")

    // animate/remove list item
    liItem[0].style.visibility = 'hidden';
    liItem.animate({
                opacity: 0,
                height: 0
              }, 300, function() { liItem.remove(); });
}

cancel_action = function(event) {
    event.preventDefault();
}

function addCfRegExpValidation(inputElems) {
    for (var i = 0; i < inputElems.length; i++) {
        var lv = new LiveValidation(inputElems[i], {validMessage: ":)"});
        lv.add(Validate.Presence, {failureMessage: "required"});
        re = new RegExp(/[12]?[A-Za-z ]+[A-Za-z] ?[0-9]+:[0-9]+ ?(- ?[0-9]+(:[0-9]+)?)?$/);
        lv.add(Validate.Format,{pattern: re, failureMessage: ":("});
    }
}

$(document).ready(function() {
    // initial event binding
    $("button").click(add_input_text);
    $("#cross_refs a").click(remove_input_text);
    $("#cancel_btn").click(cancel_action);


    $("#cross_refs input.cf").autocomplete({
        source: books
    });

    addCfRegExpValidation($("#cross_refs input[type=text]"));
    var tidbit_ta = new LiveValidation("tidbit", {validMessage: ":)"});
    tidbit_ta.add(Validate.Presence, {failureMessage: "required"})
    tidbit_ta.add(Validate.Length, {minimum: 10, tooShortMessage: "too short!"})
})