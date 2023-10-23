document.addEventListener("DOMContentLoaded", function() {
    const googleButton = document.getElementById("google-sign-in-button");

    googleButton.addEventListener("click", function() {
        // Redirect to the Google sign-in page when the button is clicked
        window.location.href = "{% provider_login_url 'google' %}?next=/";
    });
});
