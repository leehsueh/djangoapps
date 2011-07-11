/*
 * NT Greek Vocabulary
 * Javascript interaction on the edit card page (editcard.html).
 * Functions referenced by js on host HTML file
 */

function removeNode(node) {
    $(node).remove();
}

/**
 * Event listener when user clicks on x to remove a related word
 */
function removeRelatedCardFromList(event) {
    event.preventDefault();
    time = 300;
    id = this.attributes['href'].nodeValue
    liNode = this.parentNode;
    $("#id_related_cards option[value=" + id + "]")[0].selected = false;
    $(this.parentNode).fadeOut(time, function() {$(liNode).remove();});
}

/**
 * Callback function for the autocomplete plugin when data is fetched
 */
function processResults(e, data, value) {
    // data is the data Object returned by ajax view
    // value is the attribute defined in parse method
    id = data['id'];
    word = value;
    bgcolor = '#BEF56E';
    if ($("#related_cards_list li a[href=" + id + "]").length == 0) {
        // select the corresponding word on the actual select multiple form component
        $("#id_related_cards option[value='" + id + "']").attr('selected', true)

        // create the DOM nodes for updating the display of related words
        liItem = document.createElement("li");
        liItem.appendChild(document.createTextNode(word));
        liItem.setAttribute('title', word);
        a = document.createElement("a");
        a.setAttribute('href',id);
        a.setAttribute('class','x_style');
        a.setAttribute('title','remove ' + word);
        a.appendChild(document.createTextNode("x"));

        // bind click event listener for removing this word
        a.onclick = removeRelatedCardFromList;

        // add word to displayed list of related words
        liItem.appendChild(a);
        $("#related_cards_list")[0].appendChild(liItem);
    } else {
        bgcolor = 'red';
    }
    // clear the input element
    e.currentTarget.value = '';

    // animate the word
    origbgcolor = $("#related_cards_list li a[href=" + id + "]").parent().css('background-color');
    $("#related_cards_list li a[href=" + id + "]").parent()
    .css('background',bgcolor).delay(500).animate({
        'background-color': origbgcolor
    });
}