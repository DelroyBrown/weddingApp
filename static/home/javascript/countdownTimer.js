// 1. Configure your target date here (assumed 2025):
const target = new Date("June 7, 2025 14:30:00").getTime();

// 2. Grab the clock container:
const clockEl = document.getElementById("clock");

// 3. Update function:
function updateCountdown() {
    const now = Date.now();
    const diff = target - now;

    // If time’s up, show a message and stop.
    if (diff <= 0) {
        clockEl.innerHTML = "<p class='expired'>The countdown is over!</p>";
        clearInterval(timerInterval);
        return;
    }

    // 4. Calculate remaining time units:
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    // 5. Render into (#clock). You can style .grid and its children in your CSS.
    clockEl.innerHTML = `
      <div class="grid">
        <span>${days}</span>
        <p>Days</p>
      </div>
      <div class="grid">
        <span>${hours}</span>
        <p>Hours</p>
      </div>
      <div class="grid">
        <span>${minutes}</span>
        <p>Minutes</p>
      </div>
      <div class="grid">
        <span>${seconds}</span>
        <p>Seconds</p>
      </div>
    `;
}

// 6. Kick off and repeat every second:
updateCountdown(); // initial call so it doesn’t wait 1s
const timerInterval = setInterval(updateCountdown, 1000);