#script.js
document.addEventListener('DOMContentLoaded', function () {
    console.log("PAWS RUNNING Game Loaded");

    // Play Button Interaction
    const playBtn = document.getElementById('play-btn');
    if (playBtn) {
        playBtn.addEventListener('click', function () {
            alert("Game Started! Earn coins and level up.");
        });
    }

    // Dynamic Coin and Level Update (Example)
    const coinsElement = document.getElementById('coins');
    const levelElement = document.getElementById('level');

    if (coinsElement && levelElement) {
        let coins = 1000;
        let level = 1;

        setInterval(() => {
            coins += 10;
            level += 1;
            coinsElement.textContent = coins;
            levelElement.textContent = level;
        }, 5000); // Update every 5 seconds
    }
});
