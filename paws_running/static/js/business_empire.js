// static/js/business_empire.js

document.addEventListener('DOMContentLoaded', function() {
    const upgradeButton = document.querySelector('#upgrade-business-button');
    if (upgradeButton) {
        upgradeButton.addEventListener('click', function() {
            alert("Upgrading your business!");
            // Add logic for upgrading business
        });
    }
});
