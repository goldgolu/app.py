// static/js/settings.js

document.addEventListener('DOMContentLoaded', function() {
    const saveSettingsButton = document.querySelector('#save-settings-button');
    if (saveSettingsButton) {
        saveSettingsButton.addEventListener('click', function() {
            alert("Settings saved!");
            // Add logic to save user settings
        });
    }
});
