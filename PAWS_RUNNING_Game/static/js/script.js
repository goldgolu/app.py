// script.js

// DOMContentLoaded इवेंट का उपयोग करके सुनिश्चित करें कि DOM पूरी तरह से लोड हो गया है
document.addEventListener('DOMContentLoaded', function() {
    console.log("Document loaded and ready!");
    
    // बटन पर क्लिक करने पर एक अलर्ट दिखाने का उदाहरण
    const playButton = document.querySelector('.button');
    if (playButton) {
        playButton.addEventListener('click', function() {
            alert("Game is starting! Good luck!");
        });
    }

    // टास्क को पूरा करने के लिए बटन पर क्लिक करने पर
    const completeTaskButtons = document.querySelectorAll('[data-task-id]');
    completeTaskButtons.forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            completeTask(taskId);
        });
    });

    // टास्क पूरा करने का फ़ंक्शन
    function completeTask(taskId) {
        fetch(`/complete_task/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Task ${taskId} completed! Reward: ${data.reward} coins.`);
                // यहाँ पर आप UI को अपडेट कर सकते हैं
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error completing task:', error);
            alert('An error occurred while completing the task.');
        });
    }

    // लीडरबोर्ड को रिफ्रेश करने का फ़ंक्शन
    const refreshLeaderboardButton = document.querySelector('#refresh-leaderboard');
    if (refreshLeaderboardButton) {
        refreshLeaderboardButton.addEventListener('click', function() {
            fetch('/leaderboard')
            .then(response => response.json())
            .then(data => {
                updateLeaderboard(data);
            })
            .catch(error => {
                console.error('Error fetching leaderboard:', error);
            });
        });
    }

    // लीडरबोर्ड को अपडेट करने का फ़ंक्शन
    function updateLeaderboard(data) {
        const leaderboardContainer = document.querySelector('.leaderboard');
        leaderboardContainer.innerHTML = ''; // पहले से मौजूद सामग्री को साफ करें
        data.forEach((entry, index) => {
            const entryElement = document.createElement('div');
            entryElement.textContent = `${index + 1}. User ID: ${entry.user_id} - Coins: ${entry.coins}`;
            leaderboardContainer.appendChild(entryElement);
        });
    }
});

// पेज लोड होते ही लीडरबोर्ड अपडेट करें
window.onload = function() {
    fetch('/leaderboard')
    .then(response => response.json())
    .then(data => updateLeaderboard(data));
}
