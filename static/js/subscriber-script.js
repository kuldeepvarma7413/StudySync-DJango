$(document).ready(function() {
    $('#subscriber-submit').on('click', function() {
        var email = $('#mc-email').val();

        $.ajax({
            url: BASE_URL,  // Use the global variable for the base URL
            method: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),  
                email: email
            },
            success: function(response) {
                $('.subscribe-message').text(response.message);
            },
            error: function(xhr, status, error) {
                console.error('AJAX Request Error:', xhr.responseText);
                console.error('Status:', status);
                console.error('Error:', error);
            }
        });
    });
});
