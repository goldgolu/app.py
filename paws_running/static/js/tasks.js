// static/js/tasks.js

document.addEventListener('DOMContentLoaded', function() {
    const completeTaskButtons = document.querySelectorAll('.complete-task-button');
    completeTaskButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert("Task completed!");
            // Add logic to mark task as completed
        });
    });
});
