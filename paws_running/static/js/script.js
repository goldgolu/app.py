// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("Document loaded and ready!");

    // Example: Handling button click for general actions
    const someButton = document.querySelector('#some-button');
    if (someButton) {
        someButton.addEventListener('click', function() {
            alert("Button clicked!");
            // Add additional functionality here
        });
    }
});
