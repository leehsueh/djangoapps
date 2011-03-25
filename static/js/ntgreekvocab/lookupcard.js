/*
 * NT Greek Vocabulary
 * Javascript interaction on the lookup card/word page (lookupcard.html).
 */

/**
 * Performs ajax request to retrieve word info corresponding to the card id
 */
function fetchCard(elementContainerId, cardId) {
    $(elementContainerId).fadeIn(500);
    $(elementContainerId).html("<p>Fetching...</p>");
    if (cardId) {
        $.ajax({
            type: "GET",
            url: "/ntgreek/card/fetch/" + cardId,
            success: function(data) {
                $(elementContainerId).fadeOut(500, function() {$(this).html(data);})
                    .delay(200).slideDown(300);
            }
        });

    } else {
        $(elementContainerId).html("cardId is empty/null.");
    }
}