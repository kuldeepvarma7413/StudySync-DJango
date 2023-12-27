function showSnackbar(message, className) {
    var snackbar = document.getElementById("snackbar");
    var snackbarText = document.getElementById("snackbar-text");
    snackbarText.innerHTML = message;
    snackbar.className = className + " show";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 3000);
}

function showSuccessSnackbar(content, type) {
    showSnackbar(content, type);
}

function showFailSnackbar(content, type) {
    showSnackbar(content, type);
}

// get csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}