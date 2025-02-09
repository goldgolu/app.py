// static/js/trading.js

document.addEventListener('DOMContentLoaded', function() {
    const tradeButton = document.querySelector('#trade-button');
    if (tradeButton) {
        tradeButton.addEventListener('click', function() {
            alert("Trading assets!");
            // Add logic for trading assets
        });
    }
});
