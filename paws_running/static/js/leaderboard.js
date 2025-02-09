// static/js/leaderboard.js

document.addEventListener('DOMContentLoaded', function() {
    const refreshLeaderboardButton = document.querySelector('#refresh-leaderboard-button');
    if (refreshLeaderboardButton) {
        refreshLeaderboardButton.addEventListener('click', function() {
            alert("Refreshing leaderboard!");
