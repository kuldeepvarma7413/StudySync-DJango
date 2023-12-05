
  document.addEventListener('DOMContentLoaded', function () {
    // Set the countdown duration in seconds (adjust as needed)
    var countdownDuration = 60; // 5 minutes in this example

    function updateTimerDisplay(seconds) {
      var minutes = Math.floor(seconds / 60);
      var remainingSeconds = seconds % 60;
      var formattedTime =
        (minutes < 10 ? '0' : '') + minutes + ':' + (remainingSeconds < 10 ? '0' : '') + remainingSeconds;
      document.getElementById('timer').textContent = 'Time remaining: ' + formattedTime;
    }

    function startTimer(duration) {
      var startTime = new Date().getTime();
      var endTime = startTime + duration * 1000;

      function update() {
        var currentTime = new Date().getTime();
        var elapsedSeconds = Math.floor((endTime - currentTime) / 1000);

        if (elapsedSeconds <= 0) {
          // Timer expired, you can handle this case
          document.getElementById('timer').textContent = 'Time expired';
          // Optionally, you can redirect the user or perform some action
          // window.location.href = '/timeout'; // Example redirection
        } else {
          updateTimerDisplay(elapsedSeconds);
          setTimeout(update, 1000);
        }
      }

      update();
    }

    // Start the timer when the page loads
    startTimer(countdownDuration);
  });

