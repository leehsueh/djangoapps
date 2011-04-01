add_input_text = function(event) {
    event.preventDefault();
    $("#cross_refs").append('<li><input type="text" name="cf" class="cf" placeholder="Enter passage"> <a>x</a></li>');
    $("#cross_refs a").click(remove_input_text);
    addCfRegExpValidation($("#cross_refs input[type=text]").last()[0]);
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

function addCfRegExpValidation(inputElem) {
    var lv = new LiveValidation(inputElem, {validMessage: ":)"});
    lv.add(Validate.Presence, {failureMessage: "required"});
    re = new RegExp(/[12]?[A-Za-z ]+[A-Za-z] ?[0-9]+:[0-9]+ ?(- ?[0-9]+(:[0-9]+)?)?$/);
    lv.add(Validate.Format,{pattern: re, failureMessage: ":("});
}

$(document).ready(function() {
    // initial event binding
    $("button").click(add_input_text);
    $("#cross_refs a").click(remove_input_text);
    $("#cancel_btn").click(cancel_action);

    addCfRegExpValidation($("#cross_refs input[type=text]")[0]);
    var tidbit_ta = new LiveValidation("tidbit", {validMessage: ":)"});
    tidbit_ta.add(Validate.Presence, {failureMessage: "required"})
    tidbit_ta.add(Validate.Length, {minimum: 10, tooShortMessage: "too short!"})
})